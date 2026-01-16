---
id: c35lceii3uuk3ktep3yjisq
title: Settings
desc: ''
updated: 1768310652636
created: 1765730329589
---

# General OS commands: 

## Ubuntu
### Public WIFI signin:
connectivity-check.ubuntu.com
example.com 

### Network connectivity: 
ip route show
ip rule show
nmcli connection show
nmcli connection show | grep -i tun
sudo nmcli connection delete "outline TUN connection"
sudo ip rule del fwmark 0x711e lookup 7113
sudo ip route flush table 7113
sudo systemctl restart NetworkManager

## MacOS
### Public wifi signin:
captive.apple.com

## Windows:
### Windows profile commands: 
Test-Path $PROFILE
New-Item -Path $PROFILE -ItemType File -Force
code  $PROFILE


