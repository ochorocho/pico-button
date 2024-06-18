from machine import Pin
import time
import network

from machine import Pin
from neopixel import NeoPixel
from time import sleep
import json
import urequests

######################################################################################
# LED SETUP

# GPIO pin used on the Pico W
pin_stripe = 28

# Number of LEDs on the stripe (Watch out. Do not use more than ~20 - otherwise you need a external/additional power supply)
leds = 18

# Initialize the LED stripe
stripe = NeoPixel(Pin(pin_stripe, Pin.OUT), leds)

# Set a LED color - R, G, B - Set color for all LEDs on the stripe
def set_leds(color = (0, 120, 0)):
    stripe.fill(color)
    stripe.write()

######################################################################################


######################################################################################
# Config file to read (copy example.config.json -> config.json)

config_file = 'config.json'

# Read config file
def read_config():
    try:
        with open(config_file) as file:
            json_content = file.read()
            time.sleep(1)
            config = json.loads(json_content)
    except OSError as e:
        config = {}

    return config
######################################################################################

######################################################################################
# WIFI SETUP

# Connect to WIFI
def do_connect(wlan_sta) -> network.WLAN:
    global server_socket

    ssid = read_config().get("ssid")
    password = read_config().get("password")

    set_leds(color = (100, 0, 0))
    print('Trying to connect to %s...' % ssid)

    wlan_sta.active(True)
    sleep(3)

    wlan_sta.connect(ssid, password)
    timeout = 15
    timeout_start = time.time()

    while time.time() < timeout_start + timeout:
        print('.', end='')
        time.sleep(0.1)
        test = 0
        if wlan_sta.isconnected():
            break
        
        if test == 5:
            raise ConnectionError("Sorry, could not connect to %s", ssid) 

    return wlan_sta

# Actually connect to WIFI see config.json
wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_sta = do_connect(wlan_sta)

######################################################################################

######################################################################################
# BUTTON SETUP

# Configure GPIO-15 as an input with a pull-up resistor
button_pin = Pin(15, Pin.IN, Pin.PULL_UP)

def read_button_state():
    # Read the state of the button pin
    if button_pin.value() == 0:
        return True
    else:
        return False

######################################################################################

# Main Loop
while True:
    if not wlan_sta.isconnected():
        # Reconnect to WIFI if not connected
        wlan_sta = network.WLAN(network.STA_IF)
        wlan_sta.active(True)
        wlan_sta = do_connect(wlan_sta)
    else:
        if read_button_state() == True:
            # If the button is pressed, set LED color and send request
            set_leds((0,100,0))
            # Send HTTP request
            response = urequests.get("https://geek-jokes.sameerkumar.website/api?format=json")
            json_response = json.loads(response.text)
            # Show the joke retrieved from the API in Pico Repl (VS Code)
            print(json_response.get('joke'))
            response.close()
            # Set LED to full on green, to signal success.
            set_leds((0,255,0))
            sleep(1)
        else:
            # Reset LEDs to default state
            set_leds((255, 135, 0))
    # Add some timeout, so the pico is not stressed out
    time.sleep(0.1)