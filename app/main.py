### Author: Raj Rijhwani aka Camopants
### Description: Displays helpful orientation assistance for drinkers
### Category: Wearables
### License: MIT

import app
import imu
import math

from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES
from app_components.tokens import line_height

THRESHOLD=2

class BarAssistApp(app.App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.orientation = None
        self.rotation_offset = 0

    def __get_orientation(self):

        acc_read = imu.acc_read()
        self.ox = float('{0:.1f}'.format(acc_read[0] * 9))
        self.oy = float('{0:.1f}'.format(acc_read[1] * 9))
        self.oz = float('{0:.1f}'.format(acc_read[2] * 9))

        orientation = 0 if self.orientation==None else self.orientation
        # vaguely upright - no action
        if self.ox>75:
            orientation = 0
        # umop apisdn
        elif self.ox<0:
            orientation = 3
        # lying down or tilted too far
        #elif abs(self.oz)>45 or self.ox>abs(self.oy):
        elif abs(self.oz)>45:
            orientation = 1
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
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays
            # open. Without it the app would close again immediately.
            self.button_states.clear()
            self.minimise()
            print('exit')

    def draw(self, ctx):
        def place_text(self, msg, l=0, r=0, g=0.5, b=0.25):
            w = ctx.text_width(msg)
            ctx.rgb(r, g, b).move_to(-(w/2), 24*l-64).text(msg)

        newo = self.__get_orientation()
        if self.orientation != newo:
            self.orientation = newo
            v = math.sqrt(self.ox*self.ox+self.oy*self.oy+self.oz*self.oz)
            print(f'({self.ox:.1f}, {self.oy:.1f}, {self.oz:.1f})')
            print(f'Orientation: {newo}')
            print(f'Vector: {v}')

            ctx.save()
            #ctx.font = ctx.get_font_name(5)
            ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
            t = f'({self.ox}, {self.oy}, {self.oz})'
            place_text(self, t)
            t= f'Orientation: {newo}'
            place_text(self, t, l=1)
            t= f'Vector: {v:.1f}'
            place_text(self, t, l=2)
            ctx.restore()


__app_export__ = BarAssistApp

##- def olabel():
##-     #ugfx.set_default_font(#ugfx.FONT_MEDIUM)
##-     ##ugfx.text(5, 160, str("{:3d}".format(orientation))+" ("+str("{:0.2f}".format(ox))+","+str("{:0.2f}".format(oy))+")", ugfx.WHITE)
##-     #ugfx.text(5, #ugfx.height() - 20, str("{:3d}".format(orientation))+" ("+str("{:0.2f}".format(ox))+","+str("{:0.2f}".format(oy))+","+str("{:0.2f}".format(oz))+")", ugfx.WHITE)
##- 
##- def screen_l0():
##-     #ugfx.clear(#ugfx.html_color(0x7c1143))
##-     #ugfx.set_default_font(#ugfx.FONT_NAME)
##-     #ugfx.text(5,  10, "No assistance ", ugfx.WHITE)
##-     #ugfx.text(5,  60, "currently ", ugfx.WHITE)
##-     #ugfx.text(5, 110, "required ", ugfx.WHITE)
##-     olabel()
##- 
##- def screen_l1():
##-     #ugfx.clear(#ugfx.html_color(0x7c1143))
##-     #ugfx.set_default_font(#ugfx.FONT_NAME)
##-     #ugfx.text(5,  10, "Please return ", ugfx.WHITE)
##-     #ugfx.text(5,  60, "to upright ", ugfx.WHITE)
##-     #ugfx.text(5, 110, "position ", ugfx.WHITE)
##-     olabel()
##- 
##- def screen_p():
##-     #ugfx.clear(#ugfx.html_color(0x7c1143))
##-     #ugfx.set_default_font(#ugfx.FONT_NAME)
##-     #ugfx.text(5,  10, "Please ", ugfx.WHITE)
##-     #ugfx.text(5,  60, "return to ", ugfx.WHITE)
##-     #ugfx.text(5, 110, "upright ", ugfx.WHITE)
##-     #ugfx.text(5, 160, "position ", ugfx.WHITE)
##-     olabel()
##- 
