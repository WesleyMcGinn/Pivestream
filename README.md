# Pivestream
A ridiculously simple livestream system for any Raspberry Pi with a Pi Cam.

_Note, however, that this livestream is **not encrypted in any way**, and that it can be easily accessed by anyone connected to your network.  This camera system is useful for simple tasks, like monitoring 3D-prints or wildlife, but is likely not suitable for home-monitoring systems or other settings that ought to require privacy.  Please keep this in mind when using this software._

## To Install:

1) Have powered Raspberry Pi with Rasperry Pi OS and Pi Camera attached.
   
2) Use SSH or a monitor to get into terminal.
   
3) Run the following command:

``` bash
curl -fsSL https://wesleymcginn.github.io/Pivestream/install.sh | sh
```

## To Use:

1) Find your Raspberry Pi's IP address by entering: `hostname -I`
   
2) Open a web browser on any device connected to the same network as the Raspberry Pi and enter your IP address followed by ":7000".  For example, if your IP address was found to be `192.169.1.100`, enter `http://192.169.1.100:7000`.

## Additional Documentation:

Want to shut down the livestream?  `http://<IP>:7000/stop`

Want to get a singular jpg snapshot instead of a mjpg?  `http://<IP>:7000/snap.jpg`

Need to access the raw mjpg stream as the image that it is without any scaling?  `http://<IP>:7000/live.mjpg`
