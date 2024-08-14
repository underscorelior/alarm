from machine import I2C, Pin 
from time import sleep
from pico_i2c_lcd import I2cLcd
import ds1307
import tm1637

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

i2c1 = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
rtc = ds1307.DS1307(i2c1, 0x68)

sevseg = tm1637.TM1637(clk=machine.Pin(5), dio=machine.Pin(4))


while True:
    dt = rtc.datetimeRTC
    lcd.putstr(f"{dt[4]:02d}:{dt[5]:02d}:{dt[6]:02d}")

    sevseg.numbers(dt[4],dt[5])
    sleep(1)
    dt = rtc.datetimeRTC
    sevseg.show(f"{dt[4]:02d}{dt[5]:02d}")
    sleep(1)

    lcd.clear()