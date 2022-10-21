#! /usr/bin/env bash

cd ~/project-22-fal-14-ops-owl
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt

systemctl restart myportfolio
