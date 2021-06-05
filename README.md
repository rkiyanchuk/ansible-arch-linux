# ansible-arch-linux

A set of Ansible playbooks for provisioning Arch Linux. Inspired by [pigmonkey/spark](https://github.com/pigmonkey/spark) playbook.

This playbook now relies on [archinstall](https://archlinux.org/packages/extra/any/archinstall/) for initial bootstrapping.

## Usage

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

2. Install archinstall.

   ```sh
   sudo pacman -Sy archinstall
   ```

3. Run guided installer.

   ```sh
   python -m archinstall guided
   ```

4. For additional packages specify `ansible git reflector`.

### Configure Arch Linux

1. Download and decompress playbook from GitHub:

    ```sh
    git clone https://github.com/rkiyanchuk/ansible-arch-linux
    cd ansible-arch-linux
    ```

2. After the reboot login into the new system, configure WiFi via `nmtui`,
   and run Ansible to install and configure full-featured Arch Linux:

    ```sh
    ansible-galaxy install kewlfft.aur
    ansible-playbook --ask-become-pass configure.yaml
    ```

## Post-setup

### Add fingerprint authentication

```sh
sudo fprint-enroll ruslan
```

### Notes

Generating SSH key:

```sh
ssh-keygen -t ed25519 -C "${USER}@${HOSTNAME}-$(date -I)"
```
