---
id: i7yhhnz456da0ec8sl6l5086
title: Git SSH
desc: ''
updated: 1765736731660
created: 1765648953593
---

# Git.SSH

## SSH Key paths
### Windows (Zephyrus): 
ssh-add C:\Users\tesla\Documents\git\keys\rezas_zephyrus_key_labdcyadro
### WSL (Zephyrus): 
ssh-add /home/tesla/Documents/git/keys/rezas_zephyrus_key_labdcyadro
### Ubuntu (Zephyrus): 
ssh-add ~/Documents/git/keys/rezas_zephyrus_key_labdcyadro

## Ubuntu (MIPT):
ssh-add /home/user/Documents/Git/Keys/id_rsa_gitlab
ssh-add /home/user/Documents/Git/Keys/id_gitlab_yadro

### MacOS (Macbook):
ssh-add /Users/reza/Documents/Git/GitHub/Key/id_rsa_github
ssh-add /Users/reza/Documents/Git/GitLab/Key/id_gitlab_yadro

### Windows (IMT):
ssh-add D:/Git/Key/id_rsa_github

### Check and Test:
ssh -T git@github.com

## Agent activation
### Ubuntu:
eval "$(ssh-agent -s)"
### Windows:
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
Get-Service ssh-agent
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"

