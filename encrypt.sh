#!/bin/bash

# Zip the secrets
zip -r secrets.zip secrets/ -i \*

# Encrypt the zip file
openssl enc -aes-256-ecb -in secrets.zip -out secrets.enc

# Delete the zip file
rm -f secrets.zip

