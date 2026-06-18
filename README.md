# Pivestream 📺️
### That simple open-source livestream system you've been looking for....

## About:
 - A livestream system for the Raspberry Pi.
 - Works with Pi Camera or USB Webcam.
 - Open source.
 - Dead simple.
 - Install with ONE command.
 - Starts automatically on boot.
 - You can also capture images from the stream super easily.

**....What more could you want?**

<hr>

## To Install:

1) Have powered Raspberry Pi with Rasperry Pi OS and camera attached.
   
2) Use SSH or a monitor to get into the CLI.
   
3) Type this and press enter:
   
``` bash
curl -fsSL https://wesleymcginn.github.io/Pivestream/install.sh | sh
```

Or, for a **USB Camera** (_not_ a Pi Camera), use this:

``` bash
curl -fsSL https://wesleymcginn.github.io/Pivestream/install.usb.sh | sh
```

## To Use:

1) Find your Raspberry Pi's IPv4 address. (You will see it at the end of Pivestream installation)
   
2) Open a web browser on any device connected to the same network as the Raspberry Pi and enter your IPv4 address followed by `:7000`.  For example, if your IP address was found to be `192.168.1.100`, enter `http://192.168.1.100:7000`.

## Additional Documentation:

`http://<IP>:7000/snap.jpg` A jpg image of the most recent frame (useful for saving pictures or doing machine vision stuff without stopping the livestream)

`http://<IP>:7000/stop` Returns nothing but stops the livestream system and server

`http://<IP>:7000/live.mjpg` The link to the actual unscaled mjpg stream (you can put this as the href for an image element in a website)

## Super advanced stuff:

Use port forwarding to see your livestream from other wifi networks.

To customize which camera you want to use or the resolution of the stream, run:

| For Pi Camera | For USB Camera |
| :-- | :-- |
| `sudo nano /usr/local/bin/pivestream.py` | `sudo nano /usr/local/bin/pivestream.usb.py` |

And find the section that says "Customizable" above it.  You can edit any of the variables there.  Use `Ctrl + o` + `ENTER` + `Ctrl + x` to save and exit.  Reboot your Pi (`sudo reboot`) to apply any changes.

## Questions?

Write an issue and I will get back to you shortly.
