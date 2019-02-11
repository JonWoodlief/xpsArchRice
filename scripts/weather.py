#!/usr/bin/env python3
#
# Weather blocklet script for i3blocks

import os
from pyowm import OWM

# Set the api key before using this script
# name a file owm-api-key and paste your key into there

with open(os.path.expanduser("~/.rice/scripts/owm-api-key")) as f:
    api_key = f.read()[:-1]

def get_icon(wtype):
	FA_SUN = "\uf0a3"
	FA_MOON = "\uf186"
	FA_CLOUD = "\uf0c2"
	FA_UMBRELLA = "\uf0e9"
	FA_LIGHTNING = "\uf0e7"
	FA_ASTERIKS = "\uf069"
	FA_ALIGN_LEFT = "\uf036"
	FA_UNLINK = "\uf127"
	
	yellow = "#b58900"
	blue = "#268bd2"
	white = "#ffffff"
	color = ""

	# get icon according to weather condition codes
	# http://openweathermap.org/weather-conditions

	if wtype.startswith('01'):
		if wtype[2] == 'd':
			icon = FA_SUN
			color = yellow
		else:
			icon = FA_MOON
			color = yellow
	elif wtype.startswith('02'):
		# few clouds
		if wtype[2] == 'd':
			icon = FA_SUN
		else:
			icon = FA_MOON
	elif wtype.startswith('03'):
		# scattered clouds
		icon = FA_CLOUD
	elif wtype.startswith('04'):
		# broken clouds
		icon = FA_CLOUD
	elif wtype.startswith('09'):
		# shower rain
		icon = FA_CLOUD
		color = blue
	elif wtype.startswith('10'):
		# rain
		icon = FA_UMBRELLA
		color = blue
	elif wtype.startswith('11'):
		# thunderstorm
		icon = FA_LIGHTNING
		color = yellow
	elif wtype.startswith('13'):
		# Snowy
		icon = FA_ASTERIKS
		color = white
	elif wtype.startswith('50'):
		# Misty
		icon = FA_ALIGN_LEFT
	else:
		# Unknown
		icon = FA_UNLINK
	return icon, color


city_id  = os.environ.get('BLOCK_INSTANCE')
if not city_id:
	# Defaults to London, UK
	city_id = 4460243

try:  # connect
	owm = OWM(api_key)
	obs = owm.weather_at_id( int(city_id) )
	w = obs.get_weather()
except Exception:
	# If api call failed, shows error message
	FA_UNLINK = "uf127</span>"
	text = FA_UNLINK + " NO CONNECTION"
	print(text)
	print(text)

icon, color = get_icon(w.get_weather_icon_name())
temp = w.get_temperature('fahrenheit')['temp']
temp = str(round(temp)).rjust(3)

if color:
    text = "<span font='FontAwesome' color='" + color + "'>" + icon + "</span>" + temp
else:
    text = "<span font='FontAwesome'>" + icon + "</span>" + temp

# Degree symbol
text += '\u00b0'

print(text)
print(text)
