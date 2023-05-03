# Window to the Sky
A program that displays the weather forecast for Japan, the moon constellations, and their explanations.

# How to get it
https://github.com/sougetuOte/Weather_Moon_Stars
Please git clone or download the installer from
You can also download the installer from https://www.amateur-magician.life/
You can also download the installer from
If you are not familiar with the Internet, this may be easier.

# License
Copyright (c) 2023 sougetuOte
Released under the MIT license
https://opensource.org/licenses/mit-license.php

# Usage
This is a program to get weather forecasts, moon constellations, and their explanations. I made this program because it is troublesome to look up and copy and paste the information when writing a diary.
When you enter a city name in Japanese or alphabet and press a button, the weather forecast, moon constellations, and their explanations are output to the text area and clipboard.
That's all there is to it.

# Caution
It uses OpenWeather( https://openweathermap.org/ ) API, so users need to get APIKEY and register it.
To be honest, the accuracy is low. I really wanted to be able to use JMA data, but I was disappointed. Information wanted.

# How to use
Installation instructions are in install.txt
After starting the program, enter the name of the city and specify the date of the data you want. Finally, press the button and the data will be pasted into the text area and clipboard.

# File Structure
main.py: Entry point for the application; initializes and executes the GUI.
weather_gui.py: Defines the GUI using wxPython.
weather_api.py: Retrieve XML data from JMA and parse it to get weather information.
moon_age.py: provides the logic for calculating the age of the moon.
astrology.py: Provides astrological moon signs and explanations. astrology.py: reads external text files.
clipboard.py: provides utilities to copy text to the clipboard.
config.py: Provides application configuration information. This includes the path to external text files.
astrology_data.json: Contains data about astrology constellations.
app_config.ini:Contains the OpenWeather API key and the file name of the astrology data.
README.md: This file.
INSTALL.txtInstallation instructions are described.

# Contact
Twitter: https://twitter.com/ETM08214742
e-mail: magician@amateur-magician.life