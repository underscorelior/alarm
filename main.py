from machine import I2C, Pin, PWM, ADC
from time import sleep
from pico_i2c_lcd import I2cLcd
import ds1307
import tm1637
from menu import MainMenu, SettingsMenu


#### SETUP DEVICES ####
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

i2c1 = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)
rtc = ds1307.DS1307(i2c1, 0x68)

sevseg = tm1637.TM1637(clk=machine.Pin(5), dio=machine.Pin(4))

buzzer = PWM(Pin(15))

joystick = (ADC(Pin(27)), ADC(Pin(26)), Pin(16, Pin.IN, Pin.PULL_UP))

lcd.custom_char(0, bytearray([ 
 0x00,
  0x08,
  0x0C,
  0x0E,
  0x0E,
  0x0C,
  0x08,
  0x00]))

#### 7SEG DISPLAY + ALARM #### 
def display_time(dt, colon = False):
    if colon:
        sevseg.numbers(dt[4],dt[5])
    else:
        sevseg.show(f"{dt[4]:02d}{dt[5]:02d}")

def manage_alarm(dt):
    pass

#### JOYSTICK #### 
CENTER = 32759
def handle_horiz(): # -1 = center, 0 = left, 1 = right
    value = joystick[0].read_u16()

    if value < (CENTER * 2 / 3): # If is lesser than 2/3 (left)
        return 0
    elif value < (CENTER * 4 / 3): # If is greater than 4/3 (right)
        return -1
    else: # Otherwise (center)
        return 1 

def handle_vert(): # -1 = center, 1 = down, 0 = up
    value = joystick[1].read_u16()

    if value < (CENTER * 2 / 3): 
        return 1
    elif value < (CENTER * 4 / 3):
        return -1
    else:
        return 0

def handle_press(): # 0 = not pressed, 1 = pressed
    if joystick[2].value() == 1:
        return 0
    else:
        return 1


#### MAIN LOOP ####
rerender = False
colon = 0
menu = MainMenu(lcd, {'Skip': SettingsMenu(lcd), 'Settings': SettingsMenu(lcd), 'Alarm': SettingsMenu(lcd)})

menu.draw_menu()

while True:
    dt = rtc.datetimeRTC
    display_time(dt, colon > 1)
    rerender = menu.handle_joystick(handle_horiz(), handle_vert())
    new = menu.handle_press(handle_press())

    if new:
        menu = new

        menu.draw_menu()
    
    if rerender:
        menu.draw_menu()
    
    sleep(0.5)
    colon = (colon + 1) % 4
    rerender = False




#### IDEAS ####
# Menu:
## Change -> Used for changing time
    ## Shows up on the 4 digit maybe, and if you go vertically with joystick it allows you to change it up or down.
    ## If you go horiz it changes HH to MM and vice versa.
    ## Indicates which is used by blinking the one that is being edited
    ## Asks if it is for one day or a permanent change
## Skip -> Skips next day
    ## Asks for confirmation
## Settings:
    ## Allows you to change the variables related to the game
    ## Change the volume of the alarm clock, with a preview sound playing
    ## Change the days it is active on, like below
    """
      M T W T F S S
      ^   ^   ^   ^ 
    """

# Game:
## Picks between 3 games randomly:
    ## Math:
        ## Puts a customizable amount of math problems to be solved.
    ## Capitals:
        ## Guess country capital with the abcd of the keypad.
    ## Memory:
        ## Shows arrows on the LCD, you are required to memorize and do with joystick.