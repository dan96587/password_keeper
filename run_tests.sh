#!/bin/bash

# This script runs a number of trials cracking the password vault stored
# by password_keeper using the crack.sh script and timing the trials 
# so it can report the number of CPU-seconds spent (excluding time
# spent waiting). It chooses a different master password from a file
# each time.

exec 3>&1

for i in {1..5}; do
  echo -e "\n\nRUN $i\n\n"
  rm -r ~/.wallets
  declare password=`sort -R passwords.txt | head -n1`
  echo -e "$password\n$password\nexit\n" | python3 main.py > /dev/null
  echo "Master password set to $password"
  echo -e "\nRunning password cracker..."
  result=$( { /usr/bin/time -f "%S %U" ./crack.sh 1>&3; } 2>&1 )
  sys=$(echo $result | cut -d' ' -f1)
  user=$(echo $result | cut -d' ' -f2)
  time=$(echo $sys + $user | bc)
  echo "Cracked in $time seconds"
done

exec 3>&-

