Archible
========

Ansible playbook for provisioning Arch Linux.


Usage
=====

Boot into Live Arch Linux.

Download and decompress playbook from GitHub:

```
curl -L https://github.com/zoresvit/archible/tarball/master | tar xz
cd zoresvit-archible…
```

Install Ansible with Python 2 and passlib for creating password:

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
