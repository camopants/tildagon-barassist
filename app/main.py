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
        self.orientation = None
        self.rotation_offset = 0
        self.led_control = False

    def __get_orientation(self):

        acc_read = imu.acc_read()
        self.ox = float('{0:.1f}'.format(acc_read[0] * 9))
        self.oy = float('{0:.1f}'.format(acc_read[1] * 9))
        self.oz = float('{0:.1f}'.format(acc_read[2] * 9))

        self.pointer = -atan2(-self.oy, -self.ox)/pi*6 + 0.5 # light slot
        if self.pointer < 0:
            self.pointer += 12

        orientation = 0 if self.orientation==None else self.orientation
        # vaguely upright - no action
        if self.ox>75:
            orientation = 0
        # lying down or tilted too far
        elif abs(self.oz)>45:
            orientation = 1
        else:
            weighting = min(1.0, int(abs(10 - acc_read[2])) / 9)
            self.rotation_offset = (atan2(acc_read[1], acc_read[0])) * weighting

            # umop apisdn
            if self.ox<0:
                orientation = 3
            #elif abs(self.oz)>45 or self.ox>abs(self.oy):
            elif abs(self.oy)>abs(self.ox):
            # sideways left
                if self.oy<0:
                    orientation = 2
                # sideways right
                else:
                    orientation = 4
        return orientation

    #def update(self, delta):
    def update(self, _):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            print('clear buttons')
            self.button_states.clear()
            print('re-enable pattern')
            if self.led_control:
                eventbus.emit(PatternEnable())
                self.led_control = False
            print('minimise')
            self.minimise()
            return
        else:
            if not self.led_control:
                print('disable pattern')
                eventbus.emit(PatternDisable())
                self.led_control = True

# messages:
# No assistance currently required
# Please return to the upright position

    def draw(self, ctx):
        def place_text(self, msg, l=0, r=0, g=0.5, b=0.25):
            w = ctx.text_width(msg)
            ctx.rgb(r, g, b).move_to(-(w/2), 24*l-64).text(msg)

        newo = self.__get_orientation()
        if self.orientation != newo:
            self.orientation = newo
            m1 = f'({self.ox:.1f}, {self.oy:.1f}, {self.oz:.1f})'
            m2 = f'Orientation: {newo}'
            m3 = f'Pointer: {self.pointer:.2f}'

            ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
            place_text(self, m1, l=2)
            place_text(self, m2, l=3)
            place_text(self, m3, l=4)

            print(m1)
            print(m2)
            print(m3)

        self.set_leds()

    def set_leds(self):
        if not self.led_control:
            print('disable pattern')
            eventbus.emit(PatternDisable())
            self.led_control = True

        null_colour = (0, 0, 0)

        if self.orientation==0:
            led_colour = (0, 63, 0)
        else:
            led_colour = (63, 0, 0)

        # turn everything on (flat on back)
        if self.orientation==1:
            for i in range(1, 13):
                tildagonos.leds[i] = led_colour
        else:
            for i in range(1, 13):
                tildagonos.leds[i] = null_colour
            b1 = int(self.pointer)
            v2 = self.pointer - b1
            v1 = 1 - v2
            b2 = b1 + 1
            if b1<1:
                b1 = 12
            c1 = tuple([int(v1 * c) for c in led_colour])
            c2 = tuple([int(v2 * c) for c in led_colour])
            #print(f"[{b1}:{c1}]; [{b2}:{c2}]")
            tildagonos.leds[b1] = c1
            tildagonos.leds[b2] = c2

        tildagonos.leds.write()

__app_export__ = BarAssistApp

