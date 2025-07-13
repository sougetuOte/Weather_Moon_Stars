import wx
import sys
import os

# Add the src directory to the path so relative imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.weather_gui import WeatherForecastFrame

# アプリの起動を行う
if __name__ == "__main__":
    app = wx.App()
    frame = WeatherForecastFrame(None, title="お空の窓")
    frame.Show()
    app.MainLoop()