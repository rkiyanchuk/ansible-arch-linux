ansible-arch-linux
==================

A set of Ansible playbooks for provisioning Arch Linux.

Inspired by: https://github.com/pigmonkey/spark

Usage
=====

1. Download and verify latest ArchLinux ISO:

  ```
  make iso
  ```

2. Write the ISO image to a USB flash drive:

  ```
  dd bs=4M if=archlinux-$VERSION-dual.iso of=/dev/sdX status=progress && sync
  ```

3. Boot into ArchLinux Live CD.

4. Remount root partition to increase disk space for the installation.

   ```
   mount -o remount,size=1G /run/archiso/cowspace
   ```

5. Install dependencies: Ansible and `passlib` (for hashing password):

  ```
  pacman -Sy git ansible python2-passlib
  ```

6. Download and decompress playbook from GitHub:

  ```
  git clone https://github.com/zoresvit/ansible-arch-linux
  cd ansible-arch-linux
  ```


7. Run Ansible to provision base system:

  ```
  ansible-playbook -i localhost install.yml
  ```

8. After the reboot login into the new system and run Ansible to install and
  configure full-featured Arch Linux:

  ```
  ansible-playbook --ask-become-pass -i localhost config.yml
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
