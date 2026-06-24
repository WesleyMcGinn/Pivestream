#!/bin/bash

echo -e "\e[30;103;1mInstalling dependencies....\e[0m"
sudo apt-get install python3-picamera2 -y > /dev/null

echo -e "\e[30;103;1mDownloading livestream script....\e[0m"
sudo wget -O /usr/local/bin/pivestream.py -q https://wesleymcginn.github.io/Pivestream/pivestream.py

echo -e "\e[30;103;1mSetting script to start automatically on boot....\e[0m"
if crontab -l 2>/dev/null | grep -qF "@reboot python3 /usr/local/bin/pivestream.py"; then
    echo "Pivestream is already set to run on boot."
else
    (crontab -l 2>/dev/null; echo "@reboot python3 /usr/local/bin/pivestream.py") | crontab -
fi

echo -e "\e[97;42;1mDone!  Reboot your pi and then access the livestream from http://$(ip -4 -br addr show | awk '/^wl/ && NF>=3 { split($3, a, "/"); print a[1] }'):7000\e[0m"

read -p "Wanna reboot now? [Y/n] " response < /dev/tty
if [[ "$response" =~ ^[yY] ]]; then
    echo -e "\e[93mRebooting in 3 seconds.\e[0m"
    echo -e "Press \e[31;1mCtrl + c\e[0m to cancel. "
    sleep 3.5
    sudo reboot
else
    echo "OK.  Reboot whenever you're ready."
fi
