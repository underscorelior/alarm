from machine import I2C, Pin, PWM
from time import sleep
from pico_i2c_lcd import I2cLcd
import ds1307
import tm1637

#### SETUP DEVICES ####
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

i2c1 = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)
rtc = ds1307.DS1307(i2c1, 0x68)

sevseg = tm1637.TM1637(clk=machine.Pin(5), dio=machine.Pin(4))

buzzer = PWM(Pin(15))


colon = True
def display_time(dt, colon = False):
    if colon:
        sevseg.numbers(dt[4],dt[5])
    else:
        sevseg.show(f"{dt[4]:02d}{dt[5]:02d}")

def manage_alarm(dt):
    pass

selected = 0 # Goes 0-3 (0 - TL, 1 - TR, 2 - BL, 3 - BR)
set_opt = ['Skip', 'Settings', 'Alarm']
lcd.custom_char(0, bytearray([ 
 0x00,
  0x08,
  0x0C,
  0x0E,
  0x0E,
  0x0C,
  0x08,
  0x00]))
def handle_menu():
    # "  " + opt[0] + spaces_to_fill + "  " + opt[1]
    # "  " + opt[2] + spaces_to_fill + "  " + opt[3]
    spacer_1 = " " * (16-(len(set_opt[0]) + len(set_opt[1]) + 2)) # Find a better way to do this
    lcd.putstr(chr(0) + set_opt[0] + spacer_1 + " " + set_opt[1])


while True:
    dt = rtc.datetimeRTC
    display_time(dt, colon)
    handle_menu()
    sleep(1)

    colon = not colon
    lcd.clear()


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