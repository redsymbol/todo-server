#!/bin/bash
set -eo pipefail
IFS=$'\n\t'

cd ansible
rm -fr venv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../vm
vagrant up
vagrant provision
