from machine import I2C, Pin, PWM, ADC
from time import sleep
from pico_i2c_lcd import I2cLcd
import ds1307
import tm1637
from menu import MainMenu, SettingsMenu, SkipMenu, AlarmMenu

#### SETUP DEVICES ####
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

i2c1 = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
rtc = ds1307.DS1307(i2c1, 0x68)

sevseg = tm1637.TM1637(clk=machine.Pin(5), dio=machine.Pin(4))

buzzer = PWM(Pin(17))

joystick = (ADC(Pin(27)), ADC(Pin(26)), Pin(16, Pin.IN, Pin.PULL_UP))

lcd.custom_char(0, bytearray([0x00, 0x08, 0x0C, 0x0E, 0x0E, 0x0C, 0x08, 0x00]))

#### KEYPAD ####
col_list = [6, 7, 8, 9]
row_list = [10, 11, 12, 13]

for x in range(0, 4):
    row_list[x] = Pin(row_list[x], Pin.OUT)
    row_list[x].value(1)

for x in range(0, 4):
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)


key_map = [
    ["D", "#", "0", "*"],
    ["C", "9", "8", "7"],
    ["B", "6", "5", "4"],
    ["A", "3", "2", "1"],
]


def Keypad4x4Read(cols, rows):
    for r in rows:
        r.value(0)
        result = [cols[0].value(), cols[1].value(), cols[2].value(), cols[3].value()]
        if min(result) == 0:
            key = key_map[int(rows.index(r))][int(result.index(0))]
            r.value(1)  # manages key kept pressed
            return key
        r.value(1)


#### 7SEG DISPLAY + ALARM ####
def display_time(dt, blink=False, sel=0, alarm=0):
    if sel:
        alarm = [alarm // 60, alarm % 60]
    if not sel:
        sevseg.show(f"{dt[4]:02d}{dt[5]:02d}", blink)
    elif sel == 1:  # Left side (HH)
        if blink:
            sevseg.show(f"  {alarm[1]:02d}", True)
        else:
            sevseg.show(f"{alarm[0]:02d}{alarm[1]:02d}", True)
    elif sel == 2:
        if blink:
            sevseg.show(f"{alarm[0]:02d}  ", True)
        else:
            sevseg.show(f"{alarm[0]:02d}{alarm[1]:02d}", True)


def manage_alarm(dt):
    pass


#### JOYSTICK ####
CENTER = 32759


def handle_horiz():  # -1 = center, 0 = left, 1 = right
    value = joystick[0].read_u16()

    if value < (CENTER * 2 / 3):  # If is lesser than 2/3 (left)
        return 0
    elif value < (CENTER * 4 / 3):  # If is greater than 4/3 (right)
        return -1
    else:  # Otherwise (center)
        return 1


def handle_vert():  # -1 = center, 1 = down, 0 = up
    value = joystick[1].read_u16()

    if value < (CENTER * 2 / 3):
        return 1
    elif value < (CENTER * 4 / 3):
        return -1
    else:
        return 0


def handle_press():  # 0 = not pressed, 1 = pressed
    if joystick[2].value() == 1:
        return 0
    else:
        return 1


mainmenu = MainMenu(
    lcd,
    {"Skip": SkipMenu(lcd), "Settings": SettingsMenu(lcd), "Alarm": AlarmMenu(lcd)},
)

#### MAIN LOOP ####
rerender = False
colon = 0
skip_days = []
menu = mainmenu
sel_sev = 0
alarm = 420  # In seconds

menu.draw_menu()

while True:
    dt = rtc.datetimeRTC
    rerender = menu.handle_joystick(handle_horiz(), handle_vert())
    key = Keypad4x4Read(col_list, row_list)

    if type(menu) is MainMenu:
        new = menu.handle_press(handle_press())
        if new:
            menu.reset()
            menu = new
            if type(menu) is SkipMenu:
                menu.set_skips(skip_days, f"{dt[0]}{dt[1]}{dt[2]+1}")
            menu.draw_menu()
    elif type(menu) is SkipMenu:
        info = menu.handle_press(handle_press())

        if info[0]:
            if info[1]:
                menu.reset()
                menu = mainmenu
                menu.draw_menu()
            else:
                skip_days.append(f"{dt[0]}{dt[1]}{dt[2]+1}")
                menu.reset()
                menu = mainmenu
                menu.draw_menu()
    elif type(menu) is AlarmMenu:
        if not sel_sev:
            sel_sev = 1
        if rerender[0]:
            sel_sev = sel_sev % 2 + 1

        if handle_vert() == 0:
            alarm = (alarm + (5 if (sel_sev - 1) else 60)) % 1440
        elif handle_vert() == 1:
            alarm = (alarm - (5 if (sel_sev - 1) else 60)) % 1440

        if menu.handle_press(handle_press()):
            sel_sev = 0
            menu = mainmenu
            menu.draw_menu()

        rerender = False

    # if key != None:
    #     print("Pressed button: " + key)

    if rerender:
        menu.draw_menu()

    display_time(dt, colon > 3, sel_sev, alarm)
    sleep(0.25)
    colon = (colon + 1) % 8
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
