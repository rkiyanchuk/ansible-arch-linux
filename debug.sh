#!/usr/bin/env bash

mount -o remount,size=1G /run/archiso/cowspace
pacman --noconfirm -Sy reflector
reflector --sort score -p https --country 'United States' --save /etc/pacman.d/mirrorlist
pacman --noconfirm -Sy git ansible python-passlib
