ansible-arch-linux
==================

A set of Ansible playbooks for provisioning Arch Linux.

Inspired by: https://github.com/pigmonkey/spark

How to run
==========

Create bootable media
---------------------

1. Download and verify latest ArchLinux ISO:

    ```
    make iso
    ```

2. Write the ISO image to a USB flash drive:

    ```
    dd bs=4M if=archlinux-$VERSION-dual.iso of=/dev/sdX status=progress && sync
    ```

Install OS
----------

1. Boot into ArchLinux Live CD and connect to the Internet (`wifi-menu` for WiFi).

2. Remount root partition to increase disk space for the installation.

    ```
    mount -o remount,size=1G /run/archiso/cowspace
    ```

3. Install dependencies: Ansible and `passlib` (for hashing password):

    ```
    pacman -Sy git ansible python-passlib
    ```

4. Download and decompress playbook from GitHub:

    ```
    git clone https://github.com/zoresvit/ansible-arch-linux
    cd ansible-arch-linux
    ```


5. Run Ansible to provision base system:

    ```
    ansible-playbook install.yml
    ```

6. After the reboot login into the new system and run Ansible to install and
  configure full-featured Arch Linux:

    ```
    ansible-playbook --ask-become-pass config.yml
    ```

Notes
=====

Generating SSH key:

```
ssh-keygen -t ed25519 -C "${USER}@${HOSTNAME}-$(date -I)"
```

TODO
====

- Fix configuration for printer discovery (Avahi, etc).
- Configure swap file.
- bootctl hooks https://wiki.archlinux.org/index.php/Systemd-boot#Configuration
- add groups to the user: realtime, docker
