#!/bin/bash
# replace the filename with your actual vpn file
# or just remove the vpn all together
openvpn --config vpn-file-here.ovpn &
sleep 5
# need the --id or --url for the main.py
python3 /app/main.py

