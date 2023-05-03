import wx
from weather_gui import WeatherForecastFrame

# アプリの起動を行う
if __name__ == "__main__":
    app = wx.App()
    frame = WeatherForecastFrame(None, title="お空の窓")
    frame.Show()
    app.MainLoop()