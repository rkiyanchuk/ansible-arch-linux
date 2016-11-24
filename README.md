Archible
========

A set of Ansible playbooks for provisioning Arch Linux.

Overview
--------

Provisioning is done in 2 stages:

1. Bootstrap ArchLinux base system.
2. Reboot into newly installed system and finish full system configuration.



Quickstart usage
================

Boot into Live ArchLinux.

Download and decompress playbook from GitHub:

```
curl -L https://github.com/zoresvit/archible/tarball/master | tar xz
cd zoresvit-archible…
```

Install Ansible with Python 2 and `passlib` (for creating password):

```
pacman -Sy ansible python2-passlib
```

Run Ansible to provision base system:

```
ansible-playbook -i localhost install.yml
```

After reboot login to the system and run Ansible to configure Arch:

```
ansible-playbook -i localhost arch.yml
```

Inspired by: https://github.com/pigmonkey/spark
