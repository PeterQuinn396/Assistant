import webcolors
import serial # or whatever
from os import name

# parse color from IFTTT

class LEDController:



    def __init__(self):
        self.port = ""
        self.brightness =5 #set default brightness

        dict = { # to be finished
            'z': self.set_off,
            'r': self.set_red,
            'w': self.set_white,
            'q': self.set_rainbow,
            'd': self.set_random,
            'x': self.set_solid,
            'l': self.set_blink,
            'm': self.set_move,


        }

        if name == 'nt': #windows
            self.port = 'COM1'
        elif name == 'posix': #linux
            self.port='dev/tty/USBxxx'
            # use lsdev on pi to look up devices
        else:
            print("Unrecognized OS")



    def led_error(self): # have strip blink red to indicate error
        with serial.Serial(port=self.port)as ser:
            ser.write('r')
            ser.write('l')

    def set_off(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('z')

    #colors
    def set_color(self, color): #look up color in webcolors file

        try:  # look up color
            rgb = webcolors.name_to_rgb(color)
            with serial.Serial(port=self.port) as ser:
                ser.write('c')  # custom colour cmd
                ser.write(rgb.red)
                ser.write(rgb.green)
                ser.write(rgb.blue)
        except:
            print('Color not found')

    def set_red(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('r')

    def set_white(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('w')

    def set_rainbow(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('q')

    def set_random(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('d')

    #animations
    def set_solid(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('x')

    def set_blink(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('l')

    def set_move(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('m')

    def set_fade(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('f')

    def set_sine(self):
        with serial.Serial(port=self.port) as ser:
            ser.write('s')

    #brightness
    def set_brightness(self,brightness):
        with serial.Serial(port=self.port) as ser:
            ser.write(str(brightness))

    def inc_brightness(self):
        self.brightness+=1
        if self.brightness>10:
            self.brightness=10
        self.set_brightness(self.brightness)

    def dec_brightness(self):
        self.brightness-=1
        if self.brightness<1:
            self.brightness=1
        self.set_brightness(self.brightness)


if __name__ == '__main__':
    cont = LEDController()
    while True:
        print(cont.dict)
        x = input("Input a char: \n")
        func = cont.dict.get(x, None)

        if func is not None:
            func()

