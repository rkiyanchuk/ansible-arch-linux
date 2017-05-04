#!/usr/bin/python

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
module: aur
short_description: Install packages from Arch User Repository (AUR)
description:
  - Install packages from AUR using `pacaur` helper. If `pacaur` is not installed the module
    falls back to downloading the package, building and installing with `makepkg` as would be done
    manually.

options:

  name:
    description:
      - Name of AUR package to be installed.

  user:
    description:
      - User to build AUR package.

"""

import os
import pwd
import shlex
import subprocess
import tarfile
import urllib
import shutil
from urlparse import urljoin

from ansible.module_utils.basic import AnsibleModule


AUR_DIR = '/tmp'
AUR_URL = 'https://aur.archlinux.org'
SNAPSHOT_DIR = '/cgit/aur.git/snapshot/'
MAKEPKG = 'sudo -u {user} makepkg --noconfirm --noprogressbar {opts}'


class AurError(Exception):
    pass


def package_installed(package):
    """Check if a package is already installed."""
    status = subprocess.call(shlex.split('pacman -Q {0}'.format(package)))
    return status == 0


def chown(directory, user):
    """Change directory owner to specified user."""
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = pwd.getpwnam(user).pw_gid
    except KeyError:
        raise AurError('User {0} does not exist'.format(user))

    os.chown(directory, uid, gid)


def remove(path):
    try:
        shutil.rmtree(path, ignore_errors=True)
        os.remove(path)
    except OSError as exc:
        if exc.strerror == 'No such file or directory':
            pass  # File is already removed, ignore.


def aur_download(package, user):
    """Download and extract AUR snapshot."""
    os.chdir(AUR_DIR)

    snapshot = '{0}.tar.gz'.format(package)
    aur_prefix = urljoin(AUR_URL, SNAPSHOT_DIR)
    snapshot_url = urljoin(aur_prefix, snapshot)

    # Try to clean up files from previous installations.
    remove(package)
    remove(snapshot)

    try:
        urllib.urlretrieve(snapshot_url, snapshot)
    except IOError:
        raise AurError('Failed to download package {0}'.format(package))

    with tarfile.open(snapshot) as tar:
        tar.extractall()

    chown(package, user)


def aur_build(package, user):
    """Build package from AUR snapshot."""
    os.chdir(os.path.join(AUR_DIR, package))

    error = subprocess.call(
        shlex.split(MAKEPKG.format(user=user, opts='-csrf')))

    if error:
        raise AurError('Failed to build package {0}'.format(package))


def aur_install(package, user):
    """Install AUR package."""
    os.chdir(os.path.join(AUR_DIR, package))

    error = subprocess.call(shlex.split(MAKEPKG.format(user=user, opts='-i')))

    if error:
        raise AurError('Failed to install package {0}'.format(package))

    # If succeeded remove clean up package files.
    remove(package)
    remove('{0}.tar.gz'.format(package))


def main():
    """Main Ansible module function."""
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            user=dict(required=False, default=os.environ.get('USER')),
        ),
        supports_check_mode=True
    )

    package = module.params['name']
    user = module.params['user']

    if module.check_mode:
        if package_installed(package):
            module.exit_json(
                changed=False,
                msg='Package {0} already installed'.format(package))
        else:
            module.exit_json(
                changed=True,
                msg='Package {0} would be installed'.format(package))

    try:
        aur_download(package, user)
        aur_build(package, user)
        aur_install(package, user)
    except AurError as exc:
        module.fail_json(msg=exc.message)

    module.exit_json(msg='Package {0} installed'.format(package))


if __name__ == "__main__":
    main()
