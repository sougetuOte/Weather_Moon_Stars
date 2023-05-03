import wx
from weather_api import get_weather_forecast
from moon_age import calculate_moon_age
from astrology import get_moon_astrology
from clipboard import copy_to_clipboard

class WeatherForecastFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.init_ui()
        
    def init_ui(self):
        self.SetSize(500, 700)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        city_label = wx.StaticText(panel, label="都市名:")
        hbox1.Add(city_label, flag=wx.RIGHT, border=8)
        self.city_input = wx.TextCtrl(panel)
        hbox1.Add(self.city_input, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.submit_button = wx.Button(panel, label="天気予報を取得")
        hbox2.Add(self.submit_button)
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.result_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox3.Add(self.result_area, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        
        panel.SetSizer(vbox)
        
    def on_submit(self, event):
        city = self.city_input.GetValue()
        if not city:
            wx.MessageBox("都市名を入力してください。", "エラー", wx.OK | wx.ICON_ERROR)
            return
        
        weather_forecast = get_weather_forecast(city)
        if not weather_forecast:
            wx.MessageBox("天気予報の取得に失敗しました。都市名を確認してください。", "エラー", wx.OK | wx.ICON_ERROR)
            return

        moon_age = calculate_moon_age()
        moon_astrology, moon_astrology_description = get_moon_astrology()

        result_text = f"{city}の天気予報:\n{weather_forecast}\n\n月齢: {moon_age}\n\n月星座: {moon_astrology}\n{moon_astrology_description}"
        self.result_area.SetValue(result_text)

        copy_to_clipboard(result_text)

