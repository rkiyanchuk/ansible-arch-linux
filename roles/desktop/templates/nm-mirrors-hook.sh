#!/usr/bin/env bash

# Update pacman mirrors with reflector on new network connection.

IFACE=$1
STATUS=$2

if [[ ${STATUS} == "up" ]]; then
    reflector --sort score -p https --country "{{ country }}" --save /etc/pacman.d/mirrorlist
fi
