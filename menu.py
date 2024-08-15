def sel_chr(num, options, sel, char = chr(0), other = " "):
    return (char if sel == num else other) + options[num]

def space_between(str1, str2, spacer = " ", length = 16):
    spacing = spacer * (length - (len(str1+str2))) 
    return str1 + spacing + str2

# Options should be a dict, where key is the text to display and value is the Menu object for the next
class MainMenu:
    def __init__(self, display, options):
        self.display = display
        self.options = options
        self.selected = 0
        # self. 
    
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
                sel = vertical*2
            # else: 
                # sel = vertical*2+1 # There is no 4th option ATM, so if this case is met, do nothing
                rerender = True

        if sel == self.selected:
            rerender = False
        
        self.selected = sel

        return rerender

    def handle_press(self, press):
        print("A")
        if press:
            return self.options[list(self.options.keys())[self.selected]]
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
                sel = vertical*2
            # else: 
                # sel = vertical*2+1 # There is no 4th option ATM, so if this case is met, do nothing
                rerender = True

        if sel == self.selected:
            rerender = False
        
        self.selected = sel

        return rerender

    def handle_press(self, press):
        print("Press: " + str(press))