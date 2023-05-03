import requests
from datetime import datetime, timedelta
from config import read_config
import wx

# 天気予報を取得する
def get_weather_forecast(city_name, days_from_today=0):
    API_KEY, _ = read_config()
    if API_KEY is None:
        wx.MessageBox("APIキーが設定されていません。", "エラー", wx.OK | wx.ICON_ERROR)
        return None
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name,
        'appid': API_KEY,
        'lang': 'ja',
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        forecast_list = []

        target_date = datetime.now().date() + timedelta(days=days_from_today)
        target_datetime = datetime(target_date.year, target_date.month, target_date.day)
        
        for hour_offset in range(0, 24, 3): # 3時間おきに天気を取得する
            target_time = target_datetime + timedelta(hours=hour_offset)
            for item in data['list']:
                timestamp = item['dt_txt']
                forecast_datetime = datetime.fromisoformat(timestamp)
                if forecast_datetime == target_time:
                    weather_description = item['weather'][0]['description']
                    temperature = item['main']['temp']

                    forecast_list.append(
                        f"{timestamp}: 天気 - {weather_description}, 気温 - {temperature}℃"
                    )                
        
        return "\n".join(forecast_list)
    
    else:
        return f"エラー: {response.status_code}"
