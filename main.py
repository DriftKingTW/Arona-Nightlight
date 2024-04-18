import neopixel
from machine import Pin
import time
import random 

ws_pin = 26
pull_pin = Pin(27, Pin.IN, Pin.PULL_UP)
mode_pin = Pin(28, Pin.IN, Pin.PULL_UP)
led_num = 8
brightness = 1  # Adjust the brightness (0.0 - 1.0)

neoRing = neopixel.NeoPixel(Pin(ws_pin), led_num)

color_n = (20, 20, 150)
color_sr = (130, 100, 5) 
color_ssr = (100, 0, 80)

# Mode 0: lamp, mode 1: off
current_mode = 0

def set_brightness(color):
    r, g, b = color
    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)
    return (r, g, b)

def loop():
    global current_mode
    global brightness
    
    if current_mode == 0:
        color = (255, 180, 120)
        color = set_brightness(color)
        neoRing.fill(color)
        neoRing.write()
    elif current_mode == 1:
        color = (0,0,0)
        color = set_brightness(color)
        neoRing.fill(color)
        neoRing.write()
        
    if mode_pin.value() == 0:
        timer = 0
        changeMode = True
        
        while mode_pin.value() == 0:
            timer = timer + 1
            time.sleep(0.1)
            if timer > 10:
                brightness = 0.5 if brightness == 1 else 1
                print("Brightness set to:", brightness)
                changeMode = False
                color = (255, 180, 120)
                color = set_brightness(color)
                neoRing.fill(color)
                neoRing.write()
                break
            
        while mode_pin.value() == 0:
            time.sleep(0.1)
            
        if changeMode == True:
            if current_mode < 1:
                current_mode += 1
            else:
                current_mode = 0
            print("Current Mode:", current_mode)
    
    if pull_pin.value() == 0:
        pulling_animation()
        
    time.sleep(0.05)

def pulling_animation():
    global brightness
    original_brightness = brightness
    color = (10, 10, 150) 
    color2 = (100, 0, 80)
    for x in range(6):
        brightness = brightness + 0.5
        color = set_brightness(color)
        neoRing.fill(color)
        neoRing[0] = color2
        neoRing[1] = color2
        neoRing[4] = color2
        neoRing[5] = color2
        neoRing.write()
        time.sleep(0.1)
        neoRing.fill(color)
        neoRing[2] = color2
        neoRing[3] = color2
        neoRing[6] = color2
        neoRing[7] = color2
        neoRing.write()
        time.sleep(0.1)
        
    result = random.randint(0, 99)
    # 3% SR
    if result < 3:
        pulled_color = color_ssr
    # 18% R
    elif result > 2 and result < 20:
        pulled_color = color_sr
    # 79% N
    else:
        pulled_color = color_n
        
    neoRing.fill(pulled_color)
    neoRing.write()
    time.sleep(2)
    
    smooth_dim(neoRing, pulled_color)
    brightness = original_brightness

def smooth_dim(np, color, delay_ms=10, steps=100):
    r_step = color[0] / steps
    g_step = color[1] / steps
    b_step = color[2] / steps
    for i in range(steps, -1, -1):
        np.fill((int(i * r_step), int(i * g_step), int(i * b_step)))
        np.write()
        time.sleep_ms(delay_ms)


while True:
    loop()
