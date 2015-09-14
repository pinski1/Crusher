#!/usr/bin/env python 
# /etc/init.d/crusher

### BEGIN INIT INFO
# Provides:          crusher
# Required-Start:    $remote_fs $syslog $time
# Required-Stop:     $remote_fs $syslog $time
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

import time
import datetime
import math
import sqlite3
import RPi.GPIO as GPIO
import signal
import dothat.backlight
import dothat.lcd
import dothat.touch

canCrushed = 5 # sensor pin
lastDateTime = datetime.datetime.now() # last time a can was crushed
debounceTime = 5 # seconds
x = 0
intervals = ['today', 'this week', 'this month', 'this year', 'of all time']
version = '0.1.0'

# touch button handler
@dothat.touch.on(dothat.touch.BUTTON)
def handle_button(ch, evt):
	dothat.lcd.clear()
	dothat.backlight.graph_set_led_state(2, 1)
	dothat.lcd.set_cursor_position(0,0)
	dothat.lcd.write(time.strftime("%Y-%m-%d %H:%M"))	
	dothat.lcd.set_cursor_position(0, 1)
	dothat.lcd.write("Ohy! Hands off!")
	dothat.lcd.set_cursor_position(0, 2)
	dothat.lcd.write("Version: " + version)
	time.sleep(2)
	dothat.backlight.graph_off()

# touch right handler
# touch left handler
# touch up handler
# touch down handler
# touch esc handler

# can crushed handler
def handle_canCrushed(ch):
	global lastDateTime
	currentDateTime = datetime.datetime.now() # current time & date
	deltaDateTime = currentDateTime - lastDateTime
	if(deltaDateTime.total_seconds() > debounceTime):
		print "Can crushed!"
		
		conn = sqlite3.connect('/home/pi/cancrusher/cans_crushed.db')
		cursor = conn.cursor()
		cursor.execute("INSERT INTO cancrush VALUES('Can Crushed!', '" + currentDateTime.strftime('%Y-%m-%d %H:%M:%SZ') + "')") # add to database
		conn.commit()
		conn.close()
		
		# optional posting to website
			# twitter
			# adafruit.io
			# sparkfun.io
			# etc...
		
		lastDateTime = currentDateTime
		
		dothat.lcd.clear()
		dothat.lcd.set_cursor_position(0, 1)
		dothat.lcd.write("Can Crushed!")
		time.sleep(2) # delay for ~5secs?


print "Starting..."

# clear display
dothat.lcd.clear()
dothat.backlight.graph_off()
dothat.backlight.off()

# say things
dothat.lcd.set_cursor_position(0,0)
dothat.lcd.write("Starting!")

# report wifi status?

# set up GPIO interrupt for can being crushed
GPIO.setmode(GPIO.BCM)
GPIO.setup(canCrushed, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(canCrushed, GPIO.RISING, callback=handle_canCrushed)

# idle animations
while True:
	
	dothat.backlight.sweep( (x%360)/360.0)
	#dothat.backlight.set_graph(abs(math.sin(x/100.0)))
	
	if(x % 360 == 0):
		position = (x/ 360) % 5
		
		conn = sqlite3.connect('/home/pi/cancrusher/cans_crushed.db')
		cursor = conn.cursor()
		if(position == 0):
			cursor.execute("SELECT COUNT(event) FROM cancrush WHERE strftime('%Y-%m-%d', timestamp) = strftime('%Y-%m-%d', 'now')") # cans crushed today
		elif(position == 1):
			cursor.execute("SELECT COUNT(event) FROM cancrush WHERE strftime('%Y-%W', timestamp) = strftime('%Y-%W', 'now')") # cans crushed this week
		elif(position == 2):
			cursor.execute("SELECT COUNT(event) FROM cancrush WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')") # cans crushed this month
		elif(position == 3):
			cursor.execute("SELECT COUNT(event) FROM cancrush WHERE strftime('%Y', timestamp) = strftime('%Y', 'now')") # cans crushed this year
		elif(position == 4):
			cursor.execute("SELECT COUNT(event) FROM cancrush") # cans crushed all time
		else:
			print 'ERROR!'
		number = cursor.fetchone()
		conn.close()
		
		dothat.lcd.clear()
		dothat.lcd.set_cursor_position(0, 0)
		dothat.lcd.write("Cans Crushed:")
		dothat.lcd.set_cursor_position(0, 1)
		dothat.lcd.write(str(number[0]))
		dothat.lcd.set_cursor_position(0, 2)
		dothat.lcd.write(intervals[position])

	x += 1 # loop counter
	time.sleep(0.01)

GPIO.cleanup()
