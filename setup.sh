#!/bin/bash

if [ ! -d env ]; then
  virtualenv env
fi
echo "Virtualenv created"

source env/bin/activate
pip install -r requirements.txt
echo "Requirements installed"

