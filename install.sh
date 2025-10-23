#!/bin/bash

echo "Installing necessary libraries...."
sudo apt install python3-picamera2 -y

echo "Done.  Setting script to automatically start on boot...."
sudo mv ./pivestream.py /usr/local/bin/pivestream.py
if crontab -l 2>/dev/null | grep -Fq "@reboot python3 /usr/local/bin/pivestream.py"; then
    echo "This is already set to run on startup."
else
    (crontab -l 2>/dev/null; echo "@reboot python3 /usr/local/bin/pivestream.py") | crontab -
fi
python3 /usr/local/bin/pivestream.py
echo "Done!  Your pivestream is up and running!"
