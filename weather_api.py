import requests
from xml.etree import ElementTree

API_BASE_URL = "https://www.data.jma.go.jp/developer/xml/feed/regular.xml"

def get_weather_forecast(city):
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()
    except requests.RequestException:
        return None

    xml_data = ElementTree.fromstring(response.content)

    # XMLデータから都市の天気情報を取得
    weather_forecast = ""
    for area in xml_data.findall(".//area"):
        if area.find("name").text == city:
            for time in area.findall(".//time"):
                weather_forecast += f"{time.find('date').text} {time.find('hour').text}時: {time.find('weather').text}\n"

            break

    return weather_forecast if weather_forecast else None
