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

AUR packages:
```
   cower
   downgrade
   pacaur


  #- name: install essential AUR packages
  #  aur: name={{ item }} user={{ user.name }}
  #  with_items: "{{ aur_packages }}"
```

User:
```

- name: create user group
  group: name={{ user.group }} state=present

- name: create user
  user: >
    name={{ user.name }}
    group={{ user.group }}
    append=yes
    groups={{ user.groups | join(',') }}
    comment={{ user.comment }}
    password={{ hostvars.localhost.user_password }}
    update_password=on_create


- name: lock root account
  command: passwd -l root
```
