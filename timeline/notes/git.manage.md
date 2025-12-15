---
id: i7yhhnz456da0ec8sl6l5087
title: Git Manage
desc: ''
updated: 1765808398508
created: 1765650334839
---

# Git Management Commands

## Git synchronization: 
git add .
git commit -m "lol"
git push
git fetch
git pull

## Git branch management
### Stashing:
git stash save "temp changes"
git stash pop

### Rebasing:
git pull --rebase origin main

### Diff:
git status -sb
git diff -- file

### Branch:
git checkout -b reza/cocotb-env origin/cur_work_v
git push -u origin reza/cocotb-env

## Git cloning
### Clone W/O Dependencies:
git clone git@10.55.229.99:image-processing/vid_prc_lib.git
git clone "ssh://git@proxy2.cod.phystech.edu:10197/image-processing/vid_prc_lib.git"

### Clone W Dependencies:
git clone --recurse-submodules git@10.55.229.99:image-processing/plib.git

### Change default git server:
git remote set-url origin "ssh://git@proxy2.cod.phystech.edu:10197/image-processing/vid_prc_lib.git"

### Clear ignored files:
git clean -ndx
git clean -fdx