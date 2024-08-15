from machine import I2C, Pin, PWM, ADC
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

joystick = (ADC(Pin(27)), ADC(Pin(26)), Pin(16, Pin.IN, Pin.PULL_UP))

def display_time(dt, colon = False):
    if colon:
        sevseg.numbers(dt[4],dt[5])
    else:
        sevseg.show(f"{dt[4]:02d}{dt[5]:02d}")

def manage_alarm(dt):
    pass


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

sel = 0 # Goes 0-3 (0 - TL, 1 - TR, 2 - BL, 3 - BR)
lcd.custom_char(0, bytearray([ 
 0x00,
  0x08,
  0x0C,
  0x0E,
  0x0E,
  0x0C,
  0x08,
  0x00]))

def space_between(str1,str2, spacer = " ", length = 16):
    spacing = spacer * (length - (len(str1+str2))) 
    return str1 + spacing + str2

def sel_chr(num, char = chr(0), other = " "):
    opt = ['Skip', 'Settings', 'Alarm']

    return (char if sel == num else other) + opt[num]

def draw_menu():
    lcd.clear()

    lcd.putstr(space_between(sel_chr(0), sel_chr(1)))
    lcd.putstr(sel_chr(2))


def handle_menu(sel):
    init_sel = sel

    rerender = False

    if handle_horiz() != -1:
        if sel // 2 == 0:
            sel = handle_horiz()
        # else: 
            # sel = handle_horiz()+2 # There is no 4th option ATM, so if this case is met, do nothing

            rerender = True
    
    if handle_vert() != -1:
        if sel % 2 == 0: 
            sel = handle_vert()*2
        # else: 
            # sel = handle_vert()*2+1 # There is no 4th option ATM, so if this case is met, do nothing
            rerender = True
    
    if init_sel == sel:
        rerender = False

    return rerender, sel

#### MAIN LOOP ####
rerender = False
colon = True

draw_menu()

while True:
    dt = rtc.datetimeRTC
    display_time(dt, colon)

    rerender, sel = handle_menu(sel)
    
    if rerender:
        draw_menu()
    
    sleep(1)
    colon = not colon
    rerender = False

    print(f"{sel=}")



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