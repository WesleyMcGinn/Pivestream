#!/bin/bash

echo "Installing necessary libraries...."
sudo apt install python3-picamera2 -y

echo "Done.  Downloading livestream script...."
sudo wget -O /usr/local/bin/pivestream.py https://wesleymcginn.github.io/Pivestream/pivestream.py

echo "Done.  Setting script to start automatically on boot...."
if crontab -l 2>/dev/null | grep -Fq "@reboot python3 /usr/local/bin/pivestream.py"; then
    echo "This is already set to run on boot."
else
    (crontab -l 2>/dev/null; echo "@reboot python3 /usr/local/bin/pivestream.py") | crontab -
fi

echo "Done!  Reboot to start your livestream system."
