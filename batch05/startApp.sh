#!/bin/bash

trap "exit" INT TERM ERR
trap "kill 0" EXIT
source /etc/ubiquity/ros_setup.bash
IP="$(hostname -I | awk '{ print $1; }')"
# print out robot  IP
echo Machine is $IP

cd /home/ubuntu/AutoBill/CheckoutUI/client
python3 -m http.server 9000 &
cd /home/ubuntu/AutoBill/CheckoutUI/server
npm run start &
cd /home/ubuntu/AutoBill
wait