#!/bin/bash

# Unencrypt the jawn
openssl enc -d -aes-256-ecb -in secrets.enc -out secrets.zip

# Unzip the jawn
unzip secrets.zip -d secrets

# Delete the zipper jawn
rm -f secrets.zip

