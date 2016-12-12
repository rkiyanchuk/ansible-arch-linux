Archible
========

A set of Ansible playbooks for provisioning Arch Linux.

Instructions
============

Download Arch Linux ISO image and signature:

```
wget http://mirror.rackspace.com/archlinux/iso/$VERSION/archlinux-$VERSION-dual.iso
wget https://www.archlinux.org/iso/$VERSION/archlinux-$VERSION-dual.iso.sig
```

For more download options see [Arch Linux Downloads](https://www.archlinux.org/download/).

Verify the ISO image:

```
gpg --keyserver-options auto-key-retrieve --verify archlinux-$VERSION-dual.iso.sig
```

Write the ISO image to a USB flash drive:

```
dd bs=4M if=archlinux-$VERSION-dual.iso of=/dev/sdX status=progress && sync
```

Boot into Live ArchLinux.

Download and decompress playbook from GitHub:

```
curl -L https://github.com/zoresvit/archible/archive/master.tar.gz | tar xz
cd zoresvit-archible
```

Install Ansible with Python 2 and `passlib` (for creating password):

```
pacman -Sy ansible python2-passlib
```

Run Ansible to provision base system:

```
ansible-playbook -i localhost install.yml
```

After reboot login to the system and run Ansible to install and configure
full-featured ArchLinux:

```
ansible-playbook -i localhost arch.yml
```

Inspired by: https://github.com/pigmonkey/spark
