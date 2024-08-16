def sel_chr(num, options, sel, char=chr(0), other=" "):
    return (char if sel == num else other) + options[num]


def space_between(str1, str2, spacer=" ", length=16):
    spacing = spacer * (length - (len(str1 + str2)))
    return str1 + spacing + str2


# Options should be a dict, where key is the text to display and value is the Menu object for the next
class MainMenu:
    def __init__(self, display, options):
        self.display = display
        self.options = options
        self.selected = 0

    def reset(self):
        self.selected = 0

    def draw_menu(self):
        opts = list(self.options.keys())
        sel = self.selected
        lcd = self.display

        lcd.clear()
        lcd.putstr(space_between(sel_chr(0, opts, sel), sel_chr(1, opts, sel)))
        lcd.putstr(sel_chr(2, opts, sel))

    def handle_joystick(self, horizontal, vertical):
        sel = self.selected

        rerender = False

        if horizontal != -1:
            if sel // 2 == 0:
                sel = horizontal
                # else:
                # sel = horizontal+2 # There is no 4th option ATM, so if this case is met, do nothing

                rerender = True

        if vertical != -1:
            if sel % 2 == 0:
                sel = vertical * 2
                # else:
                # sel = vertical*2+1 # There is no 4th option ATM, so if this case is met, do nothing
                rerender = True

        if sel == self.selected:
            rerender = False

        self.selected = sel

        return rerender

    def handle_press(self, press):
        if press:
            return self.options[list(self.options.keys())[self.selected]]
        return False


class SkipMenu:
    def __init__(self, display):
        self.display = display
        self.selected = 0
        self.options = ["Confirm", "Back"]
        self.skips = []
        self.date = ""

    def reset(self):
        self.selected = 0

    def set_skips(self, skip_days, date):
        self.skips = skip_days
        self.date = date

    def draw_menu(self):
        lcd = self.display
        sel = self.selected
        opt = self.options
        lcd.clear()

        if self.date in self.skips:
            self.selected = 1
            sel = 1
            lcd.putstr("Already Skipped!")
            lcd.putstr("{:>16}".format(sel_chr(1, opt, sel)))
            return

        lcd.putstr("Skip Next Alarm".center(16))
        lcd.putstr(sel_chr(0, opt, sel) + " " * 3 + sel_chr(1, opt, sel))

    def handle_joystick(self, horizontal, _):
        sel = self.selected

        rerender = False
        if self.date not in self.skips:
            if horizontal != -1:
                sel = (sel - 1 + (horizontal * 2)) % 2
                rerender = True

        if sel == self.selected:
            rerender = False

        self.selected = sel

        return rerender

    def handle_press(self, press):
        if press and self.selected == 1:
            return True, 1
        if press and self.selected == 0:
            return True, 0
        return False, False


class AlarmMenu:
    def __init__(self, display):
        self.display = display
        self.options = ["Save"]

    def set_skips(self, skip_days, date):
        self.skips = skip_days
        self.date = date

    def draw_menu(self):
        lcd = self.display
        opt = self.options
        lcd.clear()

        lcd.putstr("Editing Alarm".center(16))
        lcd.putstr(sel_chr(0, opt, 0))

    def handle_joystick(self, horizontal, vertical):
        return horizontal != -1, vertical

    def handle_press(self, press):
        if press:
            return True
        return False


class SettingsMenu:
    def __init__(self, display):
        self.display = display
        self.selected = 0

    def draw_menu(self):
        lcd = self.display

        lcd.clear()
        lcd.putstr("Settings Menu")

    def handle_joystick(self, horizontal, vertical):
        sel = self.selected

        rerender = False

        if horizontal != -1:
            if sel // 2 == 0:
                sel = horizontal
                # else:
                # sel = horizontal+2 # There is no 4th option ATM, so if this case is met, do nothing

                rerender = True

        if vertical != -1:
            if sel % 2 == 0:
                sel = vertical * 2
                # else:
                # sel = vertical*2+1 # There is no 4th option ATM, so if this case is met, do nothing
                rerender = True

        if sel == self.selected:
            rerender = False

        self.selected = sel

        return rerender

    def handle_press(self, press):
        print("Press: " + str(press))
