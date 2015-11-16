#!/bin/bash

# This script reads passwords.txt line by line and prints any lines that
# successfully decrypt the passwords stored by password_keeper

let "NUMBER_WALLETS=`ls -l ~/.wallets | wc -l`-1"
declare NUMBER_FOUND=0
while read -r line; do
    echo "$line" | python3 main.py > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "$line"
        let "NUMBER_FOUND++"
        if [ $NUMBER_FOUND -eq $NUMBER_WALLETS ]; then
          exit
        fi
    fi
done < "passwords.txt"

