# ansible-arch-linux

A set of Ansible playbooks for provisioning Arch Linux.

Inspired by [pigmonkey/spark](https://github.com/pigmonkey/spark) playbook.

## How to run

### Create bootable media

1. Download and verify latest ArchLinux ISO:

    ```sh
    make iso
    ```

2. Write the ISO image to a USB flash drive:

    ```sh
    dd bs=4M if=archlinux-$VERSION-dual.iso of=/dev/sdX status=progress && sync
    ```

### Install OS

1. Boot into ArchLinux Live CD and connect to the Internet.

   Start `iwctl` prompt, then connect to WiFi with:

   ```sh
   station wlan0 connect <ssid>
   ```

2. Remount root partition to increase disk space for the installation.

    ```sh
    mount -o remount,size=1G /run/archiso/cowspace
    ```

3. Install Git and Ansible:

    ```sh
    pacman -Sy git ansible
    ```

4. Download and decompress playbook from GitHub:

    ```sh
    git clone https://github.com/rkiyanchuk/ansible-arch-linux
    cd ansible-arch-linux
    ```

5. Install dependent roles and run Ansible to provision base system:

    ```sh
    ansible-playbook install.yml
    ```

6. After the reboot login into the new system, configure WiFi via `nmtui`,
   and run Ansible to install and configure full-featured Arch Linux:

    ```sh
    ansible-galaxy install kewlfft.aur
    ansible-playbook --ask-become-pass configure.yml
    ```

## Post-setup

### Add fingerprint authentication

```sh
fprint-enroll
```

### Notes

Generating SSH key:

```sh
ssh-keygen -t ed25519 -C "${USER}@${HOSTNAME}-$(date -I)"
```