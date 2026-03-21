### Author: Raj Rijhwani
### Description: Displays helpful orientation advice for drinkers
### Category: Wearables
### License: MIT

import ugfx, pyb, buttons
from imu import IMU

ugfx.init()
ugfx.clear()
buttons.init()
old_font=ugfx.FONT_NAME
ugfx.set_default_font(ugfx.FONT_NAME)
SCREEN_DURATION = 2000

def olabel():
    ugfx.set_default_font(ugfx.FONT_MEDIUM)
    #ugfx.text(5, 160, str("{:3d}".format(orientation))+" ("+str("{:0.2f}".format(ox))+","+str("{:0.2f}".format(oy))+")", ugfx.WHITE)
    ugfx.text(5, ugfx.height() - 20, str("{:3d}".format(orientation))+" ("+str("{:0.2f}".format(ox))+","+str("{:0.2f}".format(oy))+","+str("{:0.2f}".format(oz))+")", ugfx.WHITE)

def screen_l0():
    ugfx.clear(ugfx.html_color(0x7c1143))
    ugfx.set_default_font(ugfx.FONT_NAME)
    ugfx.text(5,  10, "No assistance ", ugfx.WHITE)
    ugfx.text(5,  60, "currently ", ugfx.WHITE)
    ugfx.text(5, 110, "required ", ugfx.WHITE)
    olabel()

def screen_l1():
    ugfx.clear(ugfx.html_color(0x7c1143))
    ugfx.set_default_font(ugfx.FONT_NAME)
    ugfx.text(5,  10, "Please return ", ugfx.WHITE)
    ugfx.text(5,  60, "to upright ", ugfx.WHITE)
    ugfx.text(5, 110, "position ", ugfx.WHITE)
    olabel()

def screen_p():
    ugfx.clear(ugfx.html_color(0x7c1143))
    ugfx.set_default_font(ugfx.FONT_NAME)
    ugfx.text(5,  10, "Please ", ugfx.WHITE)
    ugfx.text(5,  60, "return to ", ugfx.WHITE)
    ugfx.text(5, 110, "upright ", ugfx.WHITE)
    ugfx.text(5, 160, "position ", ugfx.WHITE)
    olabel()

next_change = 0;
imu=IMU()
orientation = 999
upright = 99
changed = 0

while True:

    ival = imu.get_acceleration()
    ox = ival['x']
    oy = ival['y']
    oz = ival['z']

    if abs(oy) > abs(ox):
# landscape
        sr=screen_l1
        if oy<-0.1:
            newo = 0
            if abs(ox)<0.5 and abs(oz)<0.5:
# vaguely upright
                sr=screen_l0
                if upright != 1:
                    orientation = 999
                    upright = 1
            else:
# tilting too far
                sr=screen_l1
                if upright != 0:
                    orientation = 999
                    upright = 0
        elif oy>0.1:
# umop apisdn
            newo = 180

    else:
# portrait (i.e lying down)
        sr=screen_p
        if ox>0.1:
            newo = 90
        elif ox<-0.1:
            newo = 270


    if orientation != newo:
        orientation = newo
        ugfx.orientation(orientation)
        sr()

    if pyb.millis()>next_change:
        next_change = pyb.millis() + SCREEN_DURATION

    pyb.wfi()

    if buttons.is_triggered("BTN_MENU") or buttons.is_triggered("BTN_A") or buttons.is_triggered("BTN_B") or buttons.is_triggered("JOY_CENTER"):
        break;

# end of while

ugfx.set_default_font(old_font)
ugfx.clear()



