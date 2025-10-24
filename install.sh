#!/bin/bash

echo "Installing necessary libraries...."
sudo apt-get install python3-picamera2 -y > /dev/null

echo "Downloading livestream script...."
sudo wget -O /usr/local/bin/pivestream.py -q https://wesleymcginn.github.io/Pivestream/pivestream.py

echo "Setting script to start automatically on boot...."
if crontab -l 2>/dev/null | grep -qF "@reboot python3 /usr/local/bin/pivestream.py"; then
    echo "This is already set to run on boot."
else
    (crontab -l 2>/dev/null; echo "@reboot python3 /usr/local/bin/pivestream.py") | crontab -
fi

echo "Done!  Reboot your pi and then access the livestream from http://$(hostname -I | tr -d ' '):7000"
