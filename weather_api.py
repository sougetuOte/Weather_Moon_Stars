import requests
from datetime import datetime, timedelta
from config import app_config

'''
OpenWeather(https://openweathermap.org/)のAPI_KEYを利用して現在から１時間ごと、
24時間先までの天気情報を得る。
（現在が２１時であれば、今日の２１時から翌日の２０時までの予報を得る）
都市名と現在時刻を入力すると、ターミナルに出力する。
API_KEYはconfig.pyを経由し、app_config.iniから取得する。
与えられる日付時刻がローカルであることに注意
'''
def main(city_name,designated_date):
    API_KEY=app_config.get('OpenWeather','API_KEY')
    result = get_weather_forcast(city_name,designated_date,API_KEY)
    #print(result)

def get_current_weather(city_name, API_KEY):
    # 現在の天気情報を取得するAPIのエンドポイント
    url = "http://api.openweathermap.org/data/2.5/weather"
    
    # APIリクエストのパラメータ
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric',  # 温度を摂氏で取得
        'lang': 'ja'  # 日本語で結果を取得
    }
    
    # APIリクエストを送信
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"現在の天気情報の取得に失敗しました。ステータスコード: {response.status_code}"
    
    # レスポンスデータを解析
    data = response.json()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp = data['main']['temp']
    weather_description = data['weather'][0]['description']
    return f"{current_time} - 現在の温度: {temp}°C, 天気: {weather_description}"


def get_weather_forcast(city_name,designated_date,API_KEY):
    if API_KEY is None:
        print("APIキーが設定されていません。")
        return None
        # OpenWeatherMap APIのエンドポイント
    # 現在の天気情報を取得
    current_weather = get_current_weather(city_name, API_KEY)
    if current_weather.startswith("現在の天気情報の取得に失敗しました"):
        return current_weather  # 現在の天気情報の取得に失敗した場合は、そのメッセージを返す
    
    url = "http://api.openweathermap.org/data/2.5/forecast"
    
    # 指定された日付のUNIX時間を計算
    start_time = designated_date.timestamp()
    end_time = (designated_date + timedelta(days=1)).timestamp()
    
    # APIリクエストのパラメータ
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric',  # 温度を摂氏で取得
        'lang': 'ja'  # 日本語で結果を取得
    }
    
    # APIリクエストを送信
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"天気情報の取得に失敗しました。ステータスコード: {response.status_code}"
    
    # レスポンスデータを解析
    data = response.json()
    forecasts =  [current_weather]  # 現在の天気情報をリストの最初に追加
    for item in data['list']:
        # 指定された時間範囲内の予報のみを抽出
        if start_time <= item['dt'] <= end_time:
            forecast_time = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S')
            temp = item['main']['temp']
            weather_description = item['weather'][0]['description']
            forecasts.append(f"{forecast_time} - 温度: {temp}°C, 天気: {weather_description}")
    
    return "\n".join(forecasts)
    
if __name__ == "__main__":
    city_name="東京都"
    dt = datetime.today()  # ローカルな現在の日付と時刻を取得
    # print(dt)
    main(city_name,dt)
    