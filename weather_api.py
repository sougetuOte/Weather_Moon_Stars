import requests
from datetime import datetime, timedelta

def get_weather_forecast(city_name):
    api_key = "860b6bf17aa8d789839ca8006b36cd65"
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name,
        'appid': api_key,
        'lang': 'ja',
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        forecast_list = []
        
        current_date = datetime.now().date()
        tomorrow = current_date + timedelta(days=1)
        
        for item in data['list']:
            timestamp = item['dt_txt']
            date_object = datetime.fromisoformat(timestamp).date()
            
            if date_object == current_date:
                weather_description = item['weather'][0]['description']
                temperature = item['main']['temp']

                forecast_list.append(
                    f"{timestamp}: 天気 - {weather_description}, 気温 - {temperature}℃"
                )
                
            elif date_object >= tomorrow:
                break
        
        return "\n".join(forecast_list)
    
    else:
        return f"エラー: {response.status_code}"

if __name__ == "__main__":
    city_name = input("都市名を日本語またはアルファベットで入力してください: ")
#    api_key = "860b6bf17aa8d789839ca8006b36cd65"  # OpenWeatherMapのAPIキーを入力してください
    forecast = get_weather_forecast(city_name)
    print(forecast)
