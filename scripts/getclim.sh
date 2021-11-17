#!/bin/bash

netcat 192.168.15.248 12345 | while read line
 do
     match=$(echo $line | grep -c '^C')
     if [ $match -eq 1 ]; then
         echo $line
break
     fi
done