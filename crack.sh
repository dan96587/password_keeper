#!/bin/bash

# This script reads passwords.txt line by line and prints any lines that
# successfully decrypt the passwords stored by password_keeper

while read -r line; do
    echo "$line" | python3 main.py > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "$line"
    fi
done < "passwords.txt"

