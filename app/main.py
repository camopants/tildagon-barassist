### Author: Raj Rijhwani aka Camopants
### Description: Displays helpful orientation assistance for drinkers
### Category: Wearables
### License: MIT

import app
import imu

from math import pi, sqrt, atan, atan2

from app_components import clear_background
#from app_components.tokens import line_height
from events.input import Buttons, BUTTON_TYPES

from system.eventbus import eventbus
from system.patterndisplay.events import PatternEnable, PatternDisable
from tildagonos import tildagonos

THRESHOLD=2

class BarAssistApp(app.App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.__orientation = None
        self.__active = True
        self.__led_control = False

    def __get_orientation(self):
        """ identify orientation state in space from (x, y, z) vector """

        acc_read = imu.acc_read()
        self.__ox = float('{0:.1f}'.format(acc_read[0] * 9))
        self.__oy = float('{0:.1f}'.format(acc_read[1] * 9))
        self.__oz = float('{0:.1f}'.format(acc_read[2] * 9))

        self.__rotation = -atan2(self.__oy, self.__ox)
        self.__downward = self.__rotation/pi*6 + 0.5 # light slot
        if self.__downward < 0:
            self.__downward += 12

        orientation = 0 if self.__orientation==None else self.__orientation
        # vaguely upright - no action
        if self.__ox>75 and abs(self.__oy)<25:
            orientation = 0
        # lying down or tilted too far
        elif abs(self.__oz)>80:
            orientation = 1
        elif -self.__ox<75:
            orientation = 2
        else:
            orientation = 3
        return orientation

    def __set_leds(self):
        if not self.__led_control:
            print('disable pattern')
            eventbus.emit(PatternDisable())
            self.__led_control = True

        null_colour = (0, 0, 0)
        led_colour = (0, 32, 0) if self.__orientation==0 else (63, 32, 0) if self.__orientation==2 else (32, 0, 0)

        # turn everything on (flat on back)
        if self.__orientation==1:
            for i in range(1, 13):
                tildagonos.leds[i] = led_colour
        # graduated pointer indicating down
        else:
            for i in range(1, 13):
                tildagonos.leds[i] = null_colour
            b1 = int(self.__downward)
            v2 = self.__downward - b1
            b1 = (b1 + 6) % 12
            v1 = 1 - v2
            b2 = b1 + 1
            if b1<1:
                b1 = 12
            c1 = tuple([int(v1 * c) for c in led_colour])
            c2 = tuple([int(v2 * c) for c in led_colour])

            tildagonos.leds[b1] = c1
            tildagonos.leds[b2] = c2

        tildagonos.leds.write()

    def update(self, _):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            print('clear buttons')
            self.button_states.clear()
            print('re-enable pattern')
            if self.__led_control:
                eventbus.emit(PatternEnable())
                self.__led_control = False
            print('minimise and deactivate')
            self.minimise()
            self.__active = False
            return

    def draw(self, ctx):
        """ place update screen canvas """
        def place_text(self, msg, l=0, r=0, g=0.5, b=0.25):
            """ place text on relative line, and centre """
            w = ctx.text_width(msg)
            ctx.rgb(r, g, b).move_to(-(w/2), 24*l-96).text(msg)

        if not self.__active:
            print('inactive draw call')
            return

        if not self.__led_control:
            print('disable pattern')
            eventbus.emit(PatternDisable())
            self.__led_control = True

        newo = self.__get_orientation()
        #if self.__orientation != newo:
        if True:
            self.__orientation = newo
            m1 = f'({self.__ox:.1f}, {self.__oy:.1f}, {self.__oz:.1f})'
            m2 = f'Orientation: {newo}'
            if newo==1:
                m3 = f'Pointer: n/a'
            else:
                m3 = f'Pointer: {self.__downward:.2f}'

            ctx.rotate(0 if self.__orientation==1 else self.__rotation)
            ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
            if self.__orientation==0:
                ctx.font_size = 64
                place_text(self, "All good!", l=5, r=0, g=0.5, b=0)
            elif self.__orientation==3:
                place_text(self, "Please invert!", l=4, r=1, g=0, b=0)
            else:
                g = 0 if self.__orientation==1 else 0.5
                r = 1 if self.__orientation==1 else 0.5
                place_text(self, "Please return", l=3, r=r, g=g, b=0)
                place_text(self, "to the upright", l=4, r=r, g=g, b=0)
                place_text(self, "position", l=5, r=r, g=g, b=0)

            print(m1)
            print(m2)
            print(m3)

        self.__set_leds()

__app_export__ = BarAssistApp

