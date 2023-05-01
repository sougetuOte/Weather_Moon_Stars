import wx
from weather_gui import WeatherForecastFrame

if __name__ == "__main__":
    app = wx.App()
    frame = WeatherForecastFrame(None, title="天気予報と月齢・占星術情報")
    frame.Show()
    app.MainLoop()