#!/usr/bin/env python3
#
# Copyright (C) 2016 James Murphy
# Licensed under the GPL version 2 only
#
# A battery indicator blocklet script for i3blocks

import re
from subprocess import check_output

status = check_output(['acpi'], universal_newlines=True)

if not status:
    # stands for no battery found
    fulltext = "<span color='red'><span font='FontAwesome'>\uf00d \uf240</span></span>"
    percentleft = 100
else:
    # if there is more than one battery in one laptop, the percentage left is 
    # available for each battery separately, although state and remaining 
    # time for overall block is shown in the status of the first battery 
    batteries = status.split("\n")
    state_batteries=[]
    commasplitstatus_batteries=[]
    percentleft_batteries=[]
    time = ""
    for battery in batteries:
        if battery!='':
            state_batteries.append(battery.split(": ")[1].split(", ")[0])
            commasplitstatus = battery.split(", ")
            if not time:
                time = commasplitstatus[-1].strip()
                # check if it matches a time
                time = re.match(r"(\d+):(\d+)", time)
                if time:
                    time = ":".join(time.groups())
                    timeleft = " ({})".format(time)
                else:
                    timeleft = ""

            p = int(commasplitstatus[1].rstrip("%\n"))
            if p>0:
                percentleft_batteries.append(p)
            commasplitstatus_batteries.append(commasplitstatus)
    state = state_batteries[0]
    commasplitstatus = commasplitstatus_batteries[0]
    if percentleft_batteries:
        percentleft = int(sum(percentleft_batteries)/len(percentleft_batteries))
    else:
        percentleft = 0

    # stands for charging
    FA_LIGHTNING = "<span color='yellow'><span font='FontAwesome'>\uf0e7</span></span>"

    # stands for plugged in
    FA_PLUG = "<span font='FontAwesome'>\uf1e6</span>"

    # stands for using battery
    FA_BATTERY_4 = "<span font='FontAwesome'>\uf240</span>"
    FA_BATTERY_3 = "<span font='FontAwesome'>\uf241</span>"
    FA_BATTERY_2 = "<span font='FontAwesome'>\uf242</span>"
    FA_BATTERY_1 = "<span font='FontAwesome'>\uf243</span>"
    FA_BATTERY_0 = "<span font='FontAwesome'>\uf244</span>"

    FA_BATTERY= FA_BATTERY_4
    color="#859900"

    # stands for unknown status of battery
    FA_QUESTION = "<span font='FontAwesome'>\uf128</span>"

    if percentleft < 15:
        FA_BATTERY=FA_BATTERY_0
        color = "#dc322f"
    elif percentleft < 35:
        FA_BATTERY=FA_BATTERY_1
        color = "#cb4b16"
    elif percentleft < 50:
        FA_BATTERY=FA_BATTERY_2
        color = "#b58900"
    elif percentleft < 70:
        FA_BATTERY=FA_BATTERY_3
        color = "#2aa198"

    form =  '<span color="{}">{}</span>'

    if state == "Discharging":
        fulltext = form.format(color, FA_BATTERY) + " "
    elif state == "Full":
        fulltext = form.format(color, FA_LIGHTNING + FA_PLUG) + " "
        timeleft = ""
    elif state == "Unknown":
        fulltext = FA_QUESTION + " " + form.format(color, FA_BATTERY) + " "
        timeleft = ""
    else:
        fulltext = form.format(color, FA_LIGHTNING + FA_BATTERY) + " "

    
    fulltext += str(percentleft) + "%"
    fulltext += "   "
    fulltext += timeleft

print(fulltext)
print(fulltext)
