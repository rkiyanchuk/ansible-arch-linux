#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2016, Ruslan Kiianchuk <ruslan.kiianchuk@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.

"""
---
author: Ruslan Kiianchuk (@zoresvit)
module: partition
short_description: Partition block devices
description:
  - Create partitions on block devices using parted.
  Read `man parted` before usage.

options:

  dev:
    description:
      - Label or ID of block device to work on.

  table:
    description:
      - Type of disk partition table to create on the block device.
        All data will be destroyed!
    choices: ['bsd', 'loop', 'gpt', 'mac', 'msdos', 'pc98', 'sun']

  type:
    description:
      - Partition type to create (primary, logical, extended, etc).

  name:
    description:
      - Set partition name. Only works with GPT partitions.

  rm:
    description:
      - Remove partition specified by number.

  start:
    description:
      - Start of partition; use Parted units.

  end:
    description:
      - End of partition; use Parted units.

  flags:
    description:
      - Flags to enable on the partition (comma separated).

  fstype:
    description:
      - Filesystem type to be created on the partition.

  force:
    description:
      - Stop complaining and do what I say!

  lvm_group:
    description:
      - Create physical LVM volume on the partition and add it to specified
        volume group.

"""

import os
import shlex
import subprocess

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = __doc__

EXAMPLES = """
- partition: dev=/dev/sda table=gpt start=1MiB end=10GiB name=root flags=boot
- partition: dev=/dev/sdb  start=1MiB end=10GiB name=home fstype=ext4
"""


class PartitionError(Exception):
    def __init__(self, msg):
        super(PartitionError, self).__init__(msg)


class LVMError(Exception):
    def __init__(self, msg):
        super(LVMError, self).__init__(msg)


class MkfsError(Exception):
    def __init__(self, msg):
        super(MkfsError, self).__init__(msg)


def shell_cmd(cmd):
    """Execute shell command and process return values

    Low level commands like Parted suck in non-interactive mode by being very
    uninformative. So we at least wrap them to report some output to the user
    with Ansible `module.fail_json()`.

    :param cmd: Shell command to execute.
    :returns: Tuple of return code and output
              (or error message in case of failure)
    """
    prog = cmd.split()[0]
    return_code = 0
    try:
        output = subprocess.check_output(shlex.split(cmd),
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        return_code = exc.returncode
        if exc.output:
            # Replace multi-line output with single line message.
            output = exc.output.strip().replace('\n', '; ')
        else:
            output = '{0} returned error code {1}'.format(prog, return_code)

    return (return_code, output)


def is_installed(program):
    """Verify if program is installed and executable"""
    try:
        path = subprocess.check_output(['which', program]).strip()
    except subprocess.CalledProcessError as exc:
        if exc.returncode == 1:
            raise OSError('{0} program not found'.format(program))

    if not os.access(path, os.X_OK):
        raise OSError('No permissions to run {0}'.format(program))

    return True


def add_to_lvm_group(device, group):
    """Create LVM physical volume on partition"""
    is_installed('pvcreate')
    is_installed('vgcreate')
    error, output = shell_cmd('pvcreate -ffy {0}'.format(device))

    if error:
        raise LVMError(output)

    # Check if volume group exists
    error, _ = shell_cmd('vgdisplay {0}'.format(group))
    if error:  # group doesn't exist, create it with specified device.
        err, out = shell_cmd('vgcreate {0} {1}'.format(group, device))
    else:
        err, out = shell_cmd('vgextend {0} {1}'.format(group, device))

    if err:
        raise LVMError(
            'Could not add {0} to group {1}: {2}'.format(device, group, out))


def mkfs(partition, fstype, force=False):
    """Create filesystem on partition"""
    cmd_map = {
        'ext2': {'cmd': 'mkfs.ext2', 'force': '-F'},
        'ext3': {'cmd': 'mkfs.ext3', 'force': '-F'},
        'ext4': {'cmd': 'mkfs.ext4', 'force': '-F'},
        'reiserfs': {'cmd': 'mkfs.reiserfs', 'force': '-f'},
        'ext4dev': {'cmd': 'mkfs.ext4', 'force': '-F'},
        'xfs': {'cmd': 'mkfs.xfs', 'force': '-f'},
        'vfat': {'cmd': 'mkfs.vfat', 'force': str()},
        'btrfs': {'cmd': 'mkfs.btrfs', 'force': '-f'}
    }
    cmd = '{0} {1}'.format(cmd_map[fstype]['cmd'],
                           cmd_map[fstype]['force'] if force else str())
    error, output = shell_cmd('{cmd} {part}'.format(cmd=cmd, part=partition))

    if error:
        raise MkfsError(output)


class Partition(object):
    """Manipulate device partitions"""

    supported_tables = ['aix', 'amiga', 'bsd', 'dvh', 'gpt',
                        'loop', 'mac', 'msdos', 'pc98', 'sun']

    changed = False

    def __init__(self, dev_path):
        is_installed('parted')

        self.path = os.path.realpath(dev_path)

        if not os.path.exists(self.path):
            raise IOError('No such device: {0}'.format(self.path))

        self.label = self.path.split('/').pop()
        self.read_schema()

    def cmd(self, *args):
        """Execute parted command

        returns: List of lines output by parted during execution.
        raises: PartitionError in case of non-zero return code.
        """
        cmd = 'parted -sm {0} {1}'.format(self.path, ' '.join(args))

        error, output = shell_cmd(cmd)

        if error:
            raise PartitionError(output)

        lines = output.split(';\n')[:-1]  # Discard last empty line.
        return lines

    def read_schema(self):
        """Read device partitions schema"""
        lines = self.cmd('print')

        # Read device info
        units = lines[0]
        device = lines[1]
        tokens = device.split(':')

        self.info = {
            'device': self.path,
            'units': units,
            'capacity': tokens[1],
            'standard': tokens[2],
            'sector_size': {'logical': tokens[3], 'physical': tokens[4]},
            'table': tokens[5],
            'model': tokens[6],
        }

        # Read partitions
        partitions = lines[2:]
        keys = [
            'number', 'start', 'end', 'size', 'filesystem', 'name', 'flags']
        partitions = [dict(zip(keys, part.split(':'))) for part in partitions]
        self.partitions = sorted(partitions, key=lambda x: x['number'])

        return tuple(self.partitions)

    def make_table(self, table, force=False):
        if self.info['table'] and not force:
            msg = 'Partition table already exists, use `force` to override.'
            raise PartitionError(msg)
        self.cmd('mktable {0}'.format(table))
        Partition.changed = True
        self.read_schema()

    def make_part(self, ptype, start, end):
        """Make partition on disk

        :returns: Number of the created partition.

        """
        self.cmd('mkpart {type} {start} {end}'.format(type=ptype,
                                                      start=start,
                                                      end=end))
        Partition.changed = True

        # Find out number of the last created partition.
        old_parts = [p['number'] for p in self.partitions]
        self.read_schema()
        new_parts = [p['number'] for p in self.partitions]
        new = set(new_parts) - set(old_parts)

        return new.pop()

    def name(self, partition, name):
        self.cmd('name {0} {1}'.format(partition, name))
        Partition.changed = True
        self.read_schema()

    def remove(self, partition):
        self.cmd('rm {0}'.format(partition))
        Partition.changed = True
        self.read_schema()

    def set_flag(self, partition, flag, state='on'):
        self.cmd('set {0} {1} {2}'.format(partition, flag, state))
        Partition.changed = True
        self.read_schema()


def main():
    """Ansible module for disk partitioning"""

    argument_spec = {
        'dev': {'required': True, 'aliases': ['device']},
        'table': {'required': False, 'choices': Partition.supported_tables},
        'type': {'required': False, 'default': 'primary'},
        'name': {'required': False},
        'start': {'required': False},
        'end': {'required': False},
        'fstype': {'required': False},
        'flags': {'required': False},
        'force': {'required': False, 'default': 'false', 'type': 'bool'},
        'lvm_group': {'required': False},
        'rm': {'required': False, 'type': 'int'},
    }

    module = AnsibleModule(argument_spec)
    args = module.params

    try:
        device = Partition(args['dev'])

        if args['table']:
            device.make_table(args['table'], force=args['force'])

        if args['start'] and args['end']:
            partnum = device.make_part(args['type'],
                                       args['start'],
                                       args['end'])
            partition = '{0}{1}'.format(device.path, partnum)

            if args['name']:
                device.name(partnum, args['name'])

            if args['flags']:
                flags = args['flags'].split(',')
                for flag in flags:
                    device.set_flag(partnum, flag)

            if args['lvm_group']:
                add_to_lvm_group(partition, args['lvm_group'])
                Partition.changed = True

            if args['fstype']:
                mkfs(partition, args['fstype'], force=args['force'])
                Partition.changed = True

        if args['rm']:
            device.remove(args['rm'])
            Partition.changed = True

    except (PartitionError, LVMError, OSError) as exc:
        module.fail_json(msg=exc.message)

    module.exit_json(changed=Partition.changed)


if __name__ == "__main__":
    main()
