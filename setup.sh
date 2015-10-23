#!/bin/bash

if [ ! -d jam ]; then
  virtualenv jam
fi
source jam/bin/activate
pip install -r requirements.txt
