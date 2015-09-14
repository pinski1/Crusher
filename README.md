#Crusher
A Raspberry Pi powered can crusher counter.

I made this project for the can crusher in [Cambridge Makespace's](http://makespace.org/) Cakespace (the kitchen). I wanted to log how many cans were crushed and when which would also give an idea of how many were consumed.

##Hardware

To interact with the real world we need a few physical parts connected together.

###Parts

I largely bought these parts from [Pimoroni](https://shop.pimoroni.com/) but feel free to use a local supplier if you're not in the UK.

* Raspberry Pi A+ in Coupé Royale Pibow (buy [here](https://shop.pimoroni.com/collections/raspberry-pi/products/raspberry-pi-model-a-with-coupe-royale-pibow))
* SD Card ( I used a SanDisk Ultra 16Gb)
* Raspberry Pi PSU  (buy [here](https://shop.pimoroni.com/products/raspberry-pi-universal-power-supply))
* Raspberry Pi WiFi dongle  (buy [here](https://shop.pimoroni.com/products/official-raspberry-pi-wifi-dongle))
* Display-o-Tron 3000 HAT(buy [here](https://shop.pimoroni.com/products/display-o-tron-hat))
* Hall Effect sensor breakout (try [eBay](http://www.ebay.co.uk/sch/i.html?_nkw=Hall+Effect+Arduino))

###Connections
 
The next step after gathering the parts is to start putting them together!

1. Connect wires of suitable length between the Hall Effect sensor breakout and the Display-O-Tron HAT
  1. Connect R to +3V3
  2. Connect Y to GPIO 5
  3. Connect G to GND
2. Fit the Display-O-Tron HAT to the  Raspberry Pi A+ in Coupé Royale Pibow
3. Insert the Raspberry Pi WiFi dongle into the Raspberry Pi A+'s lone USB port
4. Plug in the Raspberry Pi PSU into a wall socket but also the Raspberry Pi

Done!

##Software

I'm going to assume you have have some way to get a terminal on the Raspberry Pi A+. It may be worth initially setting up the SD card on a Model B for the built in Ethernet port.

###WiFi set up

I largely used [this](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) guide to set up the Raspberry Pi WiFi dongle.

1. Type `sudo iwlist wlan0 scan` into your terminal to get the SSIDs of your WiFi AP.
2. With the SSID type `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` into your terminal.
3. then enter the following block:

```
network={
    ssid="The_ESSID_from_earlier"
    psk="Your_wifi_password"
}
```

4. Press 'Ctrl+x' then 'Y' to save the file
5. Try restarting the WiFi interface by entering `sudo ifdown wlan0` and then `sudo ifup wlan0`
6. If that doesn't work try restarting the Raspberry Pi with `sudo shutdown -r now`

###Required Modules

####SQLite3

Get & install SQLite3 with `sudo apt-get install sqlite3`

####DOTHat

Get & install Pimoroni DOTHAT

Get & install the Display-O-Tron HAT with `curl get.pimoroni.com/dot3k | bash`
<!-- https://github.com/pimoroni/dot3k -->

####GPIO

Get & install RPi.GPIO with `sudo apt-get install python-dev python-rpi.gpio`

###Starting Script on Start up

To get the script to start on start up:

1. Enter `sudo cp crusher.py /etc/init.d/crusher` into your terminal to copy the script to the init.d folder
2. Type `chmod 777 crusher` into your terminal to make the script executable
3. Then type `sudo update-rc.d crusher defaults` into your terminal to add/update the boot service

Now the script should start when the Raspberry Pi powers up. It can be started with `/etc/init.d/crusher start`, stopped with `/etc/init.d/crusher stop`, and restarted with `/etc/init.d/crusher restart`.

<!-- guide I used: http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/ -->

#To Do

Because projects aren't finished, they're just abandoned!

 * Intranet page
 * Tweet
 * Log to cloud
 * Update Makespace wiki
 * Custom Can crushing animation (Thanks [Pimoroni](https://twitter.com/pimoroni/status/643177645019164673)!) 
 * Audio fanfare!
 * Enhanced congratulation messages
 * Database error checking/backing up
 
 