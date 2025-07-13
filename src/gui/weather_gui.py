import wx
import os
from api.open_meteo_api import get_weather_for_city
from features.moon_age import get_moon_age
from features.astrology import get_moon_sign
from utils.clipboard import copy_to_clipboard
from datetime import datetime
from utils.config import app_config
from utils.error_messages import get_user_friendly_error
from utils.app_settings import app_settings

# 天気予報を表示するGUI
class WeatherForecastFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 700))
        
        # 初期化処理を整理
        self._init_services()
        self._init_ui()
        self._bind_events()
        self._load_last_search()

    def on_search(self, event):
        """検索ボタンクリック時の処理（簡潔に）"""
        city_name = self._get_city_input()
        
        if not self._validate_city_input(city_name):
            return
        
        self._show_loading_message()
        
        try:
            weather_info = self._fetch_weather_and_astronomy(city_name)
            self._display_results(weather_info)
            self._save_last_city(city_name)
        except Exception as e:
            self._handle_error(e)
    
    def _get_city_input(self):
        """都市名入力を取得"""
        return self.tc.GetValue().strip()
    
    def _validate_city_input(self, city_name):
        """入力バリデーション"""
        if not city_name:
            self._show_validation_error("都市名を入力してください。")
            return False
        return True
    
    def _show_validation_error(self, message):
        """バリデーションエラー表示"""
        self.st2.SetValue(message)
    
    def _show_loading_message(self):
        """ローディングメッセージ表示"""
        self.st2.SetValue("天気情報を取得中...")
        wx.SafeYield()  # UI更新
    
    def _fetch_weather_and_astronomy(self, city_name):
        """天気と天体情報を取得"""
        # 現在の日付と時刻を取得
        designated_date = datetime.today()
        formatted_date = designated_date.strftime('%Y/%m/%d %H:%M:%S')
        
        # 新旧システムの切り替え
        if self.use_new_service and hasattr(self, 'weather_service'):
            # 新システム（Phase 1）
            weather_data = self.weather_service.get_weather_sync(city_name)
            weather_result = self._format_new_weather_data(weather_data)
            
            # 新サービスで天体情報取得
            astronomy_data = self.astronomy_service.get_current_astronomy_data()
            moon_age = astronomy_data.moon_age
            moon_astrology_name = astronomy_data.moon_zodiac
            moon_astrology_desc = astronomy_data.zodiac_description
        else:
            # 既存システム
            weather_result = get_weather_for_city(city_name)
            
            # 既存の月齢・星座機能統合
            moon_age = get_moon_age()
            moon_astrology_name, moon_astrology_desc = get_moon_sign()
        
        return {
            'city_name': city_name,
            'formatted_date': formatted_date,
            'weather_result': weather_result,
            'moon_age': moon_age,
            'moon_astrology_name': moon_astrology_name,
            'moon_astrology_desc': moon_astrology_desc
        }
    
    def _display_results(self, weather_info):
        """結果を表示"""
        display_text = self._format_display_text(weather_info)
        self.st2.SetValue(display_text)
    
    def _format_display_text(self, weather_info):
        """表示テキストをフォーマット"""
        return (
            f"{weather_info['city_name']}の天気予報 ({weather_info['formatted_date']}):\n"
            f"{weather_info['weather_result']}\n\n"
            f"月齢: {weather_info['moon_age']:.2f}\n"
            f"月の{weather_info['moon_astrology_name']}: {weather_info['moon_astrology_desc']}"
        )
    
    def _save_last_city(self, city_name):
        """最後に検索した都市名を保存"""
        # 新しい設定管理を使用（便利メソッド）
        app_settings.set_last_city(city_name)
    
    def _handle_error(self, error):
        """エラーハンドリング（ユーザーフレンドリーなメッセージ）"""
        # ユーザーフレンドリーなエラーメッセージを取得
        user_friendly_msg = get_user_friendly_error(error)
        
        # デバッグモードの場合は技術的な詳細も表示
        debug_mode = app_settings.is_debug_mode()
        if debug_mode:
            error_msg = f"{user_friendly_msg}\n\n[詳細: {type(error).__name__}: {str(error)}]"
        else:
            error_msg = user_friendly_msg
            
        self.st2.SetValue(error_msg)

    def _init_services(self):
        """サービス層の初期化"""
        # 新しい設定管理を使用
        self.use_new_service = app_settings.is_new_service_enabled()
        if self.use_new_service:
            try:
                from services.weather_service import WeatherService
                from services.astronomy_service import AstronomyService
                self.weather_service = WeatherService()
                self.astronomy_service = AstronomyService()
            except ImportError:
                # インポートに失敗した場合は既存システムを使用
                self.use_new_service = False
    
    def _init_ui(self):
        """UI要素の初期化（既存のレイアウトを完全に保持）"""
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 都市名入力エリア
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.st1 = wx.StaticText(panel, label="都市名:")
        hbox1.Add(self.st1, flag=wx.RIGHT, border=8)
        self.tc = wx.TextCtrl(panel, value='', style=wx.TE_PROCESS_ENTER)
        hbox1.Add(self.tc, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        # ボタンエリア
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn1 = wx.Button(panel, label="実行", size=(70, 30))
        hbox2.Add(self.btn1, flag=wx.RIGHT, border=10)
        self.btn2 = wx.Button(panel, label="コピー", size=(70, 30))
        hbox2.Add(self.btn2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        # 結果表示エリア
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.st2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        hbox4.Add(self.st2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)

        vbox.Add((-1, 25))

        panel.SetSizer(vbox)
    
    def _bind_events(self):
        """イベントバインディング"""
        self.tc.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        self.btn1.Bind(wx.EVT_BUTTON, self.on_search)
        self.btn2.Bind(wx.EVT_BUTTON, self.on_copy)
    
    def _load_last_search(self):
        """前回検索した都市名を読み込み"""
        # 新しい設定管理を使用（便利メソッド）
        city_name = app_settings.get_last_city()
        self.tc.SetValue(city_name)

    def on_copy(self, event):
        text = self.st2.GetValue()  # st2からテキストを取得するためにGetValueを使用
        if text:
            copy_to_clipboard(text)
            wx.MessageBox("クリップボードにコピーしました。", "情報", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("コピーするテキストがありません。", "エラー", wx.OK | wx.ICON_ERROR)
    
    def _format_new_weather_data(self, weather_data):
        """
        新しいWeatherDataモデルを既存の表示形式に変換
        
        Phase 1では既存の表示形式を維持して、ユーザー体験を変えない
        """
        lines = []
        
        # 現在の天気
        lines.append(f"現在の天気: {weather_data.current_weather}")
        lines.append(f"気温: {weather_data.current_temp}°C")
        lines.append(f"降水確率: {weather_data.precipitation_prob}%")
        lines.append(f"風速: {weather_data.wind_speed}m/s")
        lines.append(f"湿度: {weather_data.humidity}%")
        lines.append("")
        lines.append("--- 3時間ごとの予報 ---")
        
        # 3時間ごとの予報（既存と同じ形式）
        for forecast in weather_data.get_forecast_every_n_hours(3):
            time_str = forecast.time.strftime('%H時')
            line = f"{time_str}: {forecast.weather_description} "
            line += f"{forecast.temperature}°C "
            line += f"降水{forecast.precipitation_probability}% "
            line += f"風{forecast.wind_speed}m/s"
            lines.append(line)
        
        return "\n".join(lines)
