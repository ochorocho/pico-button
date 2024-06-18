from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

# GPIO PIN the stripe is connected to (DO line on the stripe)
pin_np = 28

# LED count - Depends on how many LEDs are in use.
leds = 18

# RGB color values
color = (255,0,255)
speed = 50

# Initialize the LED stripe
stripe = NeoPixel(Pin(pin_np, Pin.OUT), leds)

# Main Loop
while True:
    for i in range (leds):
        # Loop over LEDs and switch it on one by one
        stripe[i] = color
        stripe.write()
        sleep_ms(speed)
        # Reset/turn off the current LED
        stripe[i] = (0, 0, 0)