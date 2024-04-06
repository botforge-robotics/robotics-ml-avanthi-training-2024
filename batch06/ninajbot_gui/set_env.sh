#!/bin/bash

# Get the robot ip address
echo Enter robot ip:
read IP 
Master_URL="http://$IP:11311"
# Get workstatio IP address
WSIP="$(hostname -I | awk '{ print $1; }')"
# print out robot and workstation IP
echo Robot IP is $IP
echo This pc IP is $WSIP
# set env variables for ros network communication
export ROS_IP=$WSIP
export ROS_HOSTNAME=$WSIP
export ROS_MASTER_URI=$Master_URL
