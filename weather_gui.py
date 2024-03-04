import wx
from weather_api import get_weather_forcast
from moon_age import get_moon_age
from astrology import get_moon_sign
from clipboard import copy_to_clipboard
from datetime import datetime
from config import read_config

# 天気予報を表示するGUI
class WeatherForecastFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 700))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.st1 = wx.StaticText(panel, label="都市名:")
        hbox1.Add(self.st1, flag=wx.RIGHT, border=8)
        self.tc = wx.TextCtrl(panel, value="東京都")
        hbox1.Add(self.tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn1 = wx.Button(panel, label="実行", size=(70, 30))
        hbox2.Add(self.btn1, flag=wx.RIGHT, border=10)  # ボタン間の間隔を設定
        self.btn2 = wx.Button(panel, label="コピー", size=(70, 30))
        hbox2.Add(self.btn2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.st2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        hbox4.Add(self.st2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)

        vbox.Add((-1, 25))

        panel.SetSizer(vbox)

        self.btn1.Bind(wx.EVT_BUTTON, self.on_search)
        self.btn2.Bind(wx.EVT_BUTTON, self.on_copy)

    def on_search(self, event):
        city_name = self.tc.GetValue()
        designated_date =  datetime.today()  # ローカルな現在の日付と時刻を取得
        formatted_date = designated_date.strftime('%Y/%m/%d %H:%M:%S')  # 秒までの表示にフォーマット

        API_KEY, _ = read_config()

        forecast =  get_weather_forcast(city_name,designated_date,API_KEY)
        moon_age = get_moon_age()
        moon_astrology_name, moon_astrology_desc = get_moon_sign()

        if forecast:
            self.st2.SetValue(f"{city_name}の天気予報 ({formatted_date}):\n{forecast}\n\n月齢: {moon_age:.2f}\n月の{moon_astrology_name}: {moon_astrology_desc}")
        else:
            wx.MessageBox("天気予報の取得に失敗しました。", "エラー", wx.OK | wx.ICON_ERROR)

    def on_copy(self, event):
        text = self.st2.GetValue()  # st2からテキストを取得するためにGetValueを使用
        if text:
            copy_to_clipboard(text)
            wx.MessageBox("クリップボードにコピーしました。", "情報", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("コピーするテキストがありません。", "エラー", wx.OK | wx.ICON_ERROR)
