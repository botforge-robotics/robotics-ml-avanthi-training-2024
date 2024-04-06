#!/bin/bash

# Get the robot ip address
read -p "Enter the IP address of the robot: " IP
Master_URL="http://$IP:11311"

# print out robot  IP
echo Robot IP is $IP

# set env variables for ros network communication
export ROS_IP=$IP
export ROS_HOSTNAME=$IP
export ROS_MASTER_URI=$Master_URL

