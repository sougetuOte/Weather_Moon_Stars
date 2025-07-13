import wx
from api.open_meteo_api import get_weather_for_city
from features.moon_age import get_moon_age
from features.astrology import get_moon_sign
from utils.clipboard import copy_to_clipboard
from datetime import datetime
from utils.config import app_config

# 天気予報を表示するGUI
class WeatherForecastFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 700))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.st1 = wx.StaticText(panel, label="都市名:")
        hbox1.Add(self.st1, flag=wx.RIGHT, border=8)
        city_name = app_config.get('LastSearch','CITY_NAME')
        if city_name is None:
            city_name = '東京都'
        self.tc = wx.TextCtrl(panel, value=city_name, style=wx.TE_PROCESS_ENTER)
        hbox1.Add(self.tc, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        # ENTERキーが押されたときにon_searchメソッドを実行するようにバインド
        self.tc.Bind(wx.EVT_TEXT_ENTER, self.on_search)        

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
        """天気検索処理（Open-Meteo API統合版）"""
        city_name = self.tc.GetValue().strip()
        
        # 入力バリデーション（GUI側）
        if not city_name:
            self.st2.SetValue("都市名を入力してください。")
            return
        
        # ローディング表示（ユーザビリティ向上）
        self.st2.SetValue("天気情報を取得中...")
        wx.SafeYield()  # UI更新
        
        try:
            # 現在の日付と時刻を取得
            designated_date = datetime.today()
            formatted_date = designated_date.strftime('%Y/%m/%d %H:%M:%S')
            
            # Open-Meteo API呼び出し
            weather_result = get_weather_for_city(city_name)
            
            # 既存の月齢・星座機能統合
            moon_age = get_moon_age()
            moon_astrology_name, moon_astrology_desc = get_moon_sign()
            
            # 結果統合
            combined_result = f"{city_name}の天気予報 ({formatted_date}):\n{weather_result}\n\n月齢: {moon_age:.2f}\n月の{moon_astrology_name}: {moon_astrology_desc}"
            self.st2.SetValue(combined_result)
            
            # 最後に検索した都市名を保存（既存機能）
            app_config.set('LastSearch', 'CITY_NAME', city_name)
            
        except Exception as e:
            # エラーハンドリング
            error_msg = f"天気情報の取得中にエラーが発生しました: {str(e)}"
            self.st2.SetValue(error_msg)

    def on_copy(self, event):
        text = self.st2.GetValue()  # st2からテキストを取得するためにGetValueを使用
        if text:
            copy_to_clipboard(text)
            wx.MessageBox("クリップボードにコピーしました。", "情報", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("コピーするテキストがありません。", "エラー", wx.OK | wx.ICON_ERROR)
