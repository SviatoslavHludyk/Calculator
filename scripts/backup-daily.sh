#!/bin/bash
####################################
#
# Backup to NFS mount script with
# grandfather-father-son rotation.
#
####################################

sh  /usr/local/bin/influx_bkp.sh

# What to backup. 
backup_files="/home/sh/influxdb/backup"

# Where to backup to.
dest="/mnt/backup/influxdb"

# Setup variables for the archive filename.
day=$(date +%A)

# Find which week of the month 1-4 it is.
day_num=$(date +%-d)
if (( $day_num <= 7 )); then
        week_file="influxdb-week1.tgz"
elif (( $day_num > 7 && $day_num <= 14 )); then
        week_file="influxdb-week2.tgz"
elif (( $day_num > 14 && $day_num <= 21 )); then
        week_file="influxdb-week3.tgz"
elif (( $day_num > 21 && $day_num < 32 )); then
        week_file="influxdb-week4.tgz"
fi

# Find if the Month is odd or even.
month_num=$(date +%m)
month=$(expr $month_num % 2)
if [ $month -eq 0 ]; then
        month_file="influxdb-month2.tgz"
else
        month_file="influxdb-month1.tgz"
fi

# Create archive filename.
if [ $day_num == 1 ]; then
    archive_file=$month_file
elif [ $day != "Saturday" ]; then
        archive_file="influxdb-$day.tgz"
else 
    archive_file=$week_file
fi

# Print start status message.
echo "Backing up $backup_files to $dest/$archive_file"
date
echo

# Backup the files using tar.
tar cfP $dest/$archive_file $backup_files

echo "Delete files"
rm -R /home/sh/influxdb/backup/*

# Print end status message.
echo
echo "Backup finished"
date

