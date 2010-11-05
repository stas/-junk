#!/bin/bash

FILENAME='users.txt'

for l in `cat $FILENAME`;
do
    #echo $l
    user=`echo $l | cut -d ':' -f 1`
    logins=`echo $l | cut -d ':' -f 2`
    latest_logins=`last $user | wc -l`
    #update the file
    run=`sed -i "s/$user:$logins/$user:$latest_logins/g" $FILENAME`
done;
