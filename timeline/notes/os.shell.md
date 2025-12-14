---
id: i7yhhnz456da0ec8sl6l5088
title: Shell
desc: ''
updated: 1765741386696
created: 1765650803300
---

# Ubuntu shell

## Terminal Colors: 
Text:  # FFFFFF
Background: # 242424

## shell command for current time and date: 
date +%s%3N 

## Bashrc: 
sudo nano ~/.bashrc
### Alias commands:
alias upgate='sudo apt update && sudo apt upgrade'
alias github_ssh="ssh-add ~/Documents/git/keys/rezas_zephyrus_key_github"
alias labdcyadro_ssh="ssh-add ~/Documents/git/keys/rezas_zephyrus_key_labdcyadro"
alias activate_cocotb="source ~/Documents/virtual_env/cocotb_env/bin/activate"
alias vivado='cd ~/Documents/vivado_logs && /tools/Xilinx/Vivado/2024.1/bin/vivado'
alias vitis_classic='cd ~/Documents/vivado_logs && /tools/Xilinx/Vitis/2024.1/bin/vitis -classic'
alias con_vpn="openvpn3 session-start --config /home/reza-aliasgari-renani/Documents/vpn/Reza.ovpn"
alias dis_vpn="openvpn3 session-manage --config /home/reza-aliasgari-renani/Documents/vpn/Reza.ovpn --disconnect"

## Python Virtual Environment
### Creating python virtual environment: 
python3 -m venv ~/Documents/virtual_env/my_new_env_name

## Updates and Upgrades: 
sudo apt update && sudo apt upgrade -y
sudo dpkg -i 
