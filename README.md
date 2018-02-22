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

4. Download and decompress playbook from GitHub:

  ```
  curl -L https://github.com/zoresvit/ansible-arch-linux/archive/master.tar.gz | tar -xz
  cd zoresvit-ansible-arch-linux
  ```

5. Install Ansible and `passlib` (for hashing password):

  ```
  pacman -Sy ansible python2-passlib
  ```

6. Run Ansible to provision base system:

  ```
  ansible-playbook -i localhost install.yml
  ```

7. After the reboot login into the new system and run Ansible to install and
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
