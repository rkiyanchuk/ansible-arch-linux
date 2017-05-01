Archible
========

A set of Ansible playbooks for provisioning Arch Linux.

Inspired by: https://github.com/pigmonkey/spark

How to clone:

```
   git clone https://github.com/zoresvit/archible
   cd archible
   git submodule init
   git submodule update
```

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

3. Boot into Live ArchLinux.

4. Download and decompress playbook from GitHub:

  ```
  curl -L https://github.com/zoresvit/archible/archive/master.tar.gz | tar -x
  cd zoresvit-archible
  ```

5. Install Ansible with Python 2 and `passlib` (for creating password):

  ```
  pacman -Sy ansible python2-passlib python2-pexpect
  ```

6. Run Ansible to provision base system:

  ```
  ansible-playbook -i localhost install.yml
  ```

7. After the reboot login into the system and run Ansible to install and configure
  full-featured ArchLinux:

  ```
  ansible-playbook -i localhost arch.yml
  ```


TODO
====

Fonts to show asian characters:
```
 ttf-freefont, ttf-arphic-uming, ttf-baekmuk
```

Packages
```
pacman:
  - vim

# Filesystem
  - dosfstools
  - hfsprogs
  - ntfs-3g
  - exfat-utils

# Archive
  - zip
  - unzip
  - p7zip
  - unrar
  - atool
  -
    - breeze-default-cursor-theme
    - breeze-hacked-cursor-theme

```

- Add NetworkManager hook for updating mirrors via reflector
