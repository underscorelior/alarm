from machine import I2C, Pin , PWM
from time import sleep
from pico_i2c_lcd import I2cLcd
import ds1307
import tm1637

#### SETUP DEVICES ####
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

i2c1 = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
rtc = ds1307.DS1307(i2c1, 0x68)

sevseg = tm1637.TM1637(clk=machine.Pin(5), dio=machine.Pin(4))

buzzer = PWM(Pin(15))

colon = True
def display_time(dt, colon = False):
    # lcd.putstr(f"{dt[4]:02d}:{dt[5]:02d}:{dt[6]:02d}")
    if colon:
        sevseg.numbers(dt[4],dt[5])
    else:
        sevseg.show(f"{dt[4]:02d}{dt[5]:02d}")

def manage_alarm(dt):
    pass

selected = 0 # Goes 0-3 (0 - TL, 1 - TR, 2 - BL, 3 - BR)
set_opt = ['Skip', 'Settings', 'Alarm']
lcd.custom_char(3, bytearray([ 
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
    lcd.putstr(chr(3) + set_opt[0] + spacer_1 + " " + set_opt[1])


while True:
    dt = rtc.datetimeRTC
    display_time(dt, colon)
    handle_menu()
    sleep(1)

    colon = not colon
    lcd.clear()