from machine import Pin
from time import sleep

# Initialize Board LED
led_onboard = Pin("LED", Pin.OUT)

while True:
    # LED on
    led_onboard.on()
    sleep(0.5)
    # LED off
    led_onboard.off()
    # Take a break
    sleep(1)