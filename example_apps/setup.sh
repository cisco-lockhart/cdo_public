#!/bin/bash

is_python_installed=$(brew ls --versions python)
if [[ !  -z  $is_python_installed  ]]; then
  brew upgrade python
else
  brew install python3
fi

pip3 install virtualenv
cd python
virtualenv -p python3 venv
source venv/bin/activate

cd ../node
source $(brew --prefix nvm)/nvm.sh
nvm install 6.11.1
cd report_generator
npm install
