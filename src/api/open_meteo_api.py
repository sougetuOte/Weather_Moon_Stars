"""
Open-Meteo API モジュール

OpenWeatherMap APIからOpen-Meteo APIへの移行による高精度天気予報実装
- 無料・高精度・APIキー不要
- 詳細住所対応（都城市上長飯町レベル）
- WMO天気コード対応
"""

import requests
from datetime import datetime
from typing import Tuple, Dict, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import sys
import os

# utils パッケージを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

try:
    from weather_codes import WMO_CODES
except ImportError:
    # weather_codes.py が未作成の場合の暫定対応
    WMO_CODES = {
        0: "快晴", 1: "概ね晴れ", 2: "部分的に曇り", 3: "曇り",
        45: "霧", 48: "霧氷", 51: "小雨", 53: "雨", 55: "大雨",
        61: "小雨", 63: "雨", 65: "大雨", 80: "にわか雨", 95: "雷雨"
    }


def get_coordinates(city_name: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    都市名から緯度経度を取得（詳細住所対応）
    
    Args:
        city_name (str): 都市名または詳細住所（例：「都城市上長飯町」）
    
    Returns:
        Tuple[Optional[float], Optional[float], Optional[str]]: 
        (緯度, 経度, エラーメッセージ) または (lat, lon, None)
    """
    try:
        # 入力バリデーション
        if not city_name or not city_name.strip():
            return None, None, "都市名を入力してください。"
        
        # 特殊文字のチェック（日本語・英数字・スペース・ハイフンのみ許可）
        import re
        if not re.match(r'^[a-zA-Z0-9\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F\u2B820-\u2CEAF\u2CEB0-\u2EBEF\u30000-\u3134F\-]+$', city_name.strip()):
            return None, None, "都市名には日本語、英数字、スペース、ハイフンのみ使用できます。"
        
        city_name = city_name.strip()
        
        # ユーザーエージェントは日本語プロジェクト名
        geolocator = Nominatim(user_agent="okora-no-mado", timeout=10)
        
        # 詳細住所に「日本」を追加して検索精度向上
        search_query = f"{city_name}, 日本"
        
        # 地名解決実行
        location = geolocator.geocode(search_query)
        
        if location is None:
            return None, None, f"'{city_name}' の位置情報が見つかりませんでした。正確な市区町村名を入力してください。"
        
        return location.latitude, location.longitude, None
        
    except GeocoderTimedOut:
        return None, None, "地名検索がタイムアウトしました。しばらく待ってから再試行してください。"
    except GeocoderServiceError as e:
        return None, None, f"地名検索サービスでエラーが発生しました: {str(e)}"
    except Exception as e:
        return None, None, f"地名解決中に予期しないエラーが発生しました: {str(e)}"


def get_weather_forecast(latitude: float, longitude: float) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Open-Meteo APIから天気予報データを取得
    
    Args:
        latitude (float): 緯度
        longitude (float): 経度
    
    Returns:
        Tuple[Optional[Dict], Optional[str]]: (天気データ, エラーメッセージ) または (data, None)
    """
    try:
        # Open-Meteo API URL
        url = "https://api.open-meteo.com/v1/forecast"
        
        # APIパラメータ
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'temperature_2m,precipitation_probability,weathercode,windspeed_10m,relativehumidity_2m',
            'timezone': 'Asia/Tokyo',
            'forecast_days': 1
        }
        
        # API呼び出し（5秒タイムアウト）
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code != 200:
            return None, f"天気データの取得に失敗しました。ステータスコード: {response.status_code}"
        
        data = response.json()
        
        # レスポンスの妥当性確認
        if 'hourly' not in data:
            return None, "取得した天気データの形式が正しくありません。"
        
        return data, None
        
    except requests.exceptions.Timeout:
        return None, "天気データの取得がタイムアウトしました。ネットワーク接続を確認してください。"
    except requests.exceptions.RequestException as e:
        return None, f"天気データの取得中にネットワークエラーが発生しました: {str(e)}"
    except Exception as e:
        return None, f"天気データの取得中に予期しないエラーが発生しました: {str(e)}"


def convert_wmo_code(weather_code: int) -> str:
    """
    WMO天気コードを日本語に変換
    
    Args:
        weather_code (int): WMO天気コード
    
    Returns:
        str: 日本語天気説明
    """
    return WMO_CODES.get(weather_code, f"天気情報取得中 (コード: {weather_code})")


def format_weather_data(weather_data: Dict, city_name: str) -> str:
    """
    取得した天気データを表示用フォーマットに変換
    
    Args:
        weather_data (Dict): Open-Meteo APIからの天気データ
        city_name (str): 都市名
    
    Returns:
        str: フォーマット済み天気情報
    """
    try:
        hourly_data = weather_data['hourly']
        times = hourly_data['time']
        temperatures = hourly_data['temperature_2m']
        precipitation_probs = hourly_data['precipitation_probability']
        weather_codes = hourly_data['weathercode']
        wind_speeds = hourly_data['windspeed_10m']
        humidities = hourly_data['relativehumidity_2m']
        
        # 現在時刻取得
        current_time = datetime.now()
        
        # フォーマット済み結果
        result_lines = [f"{city_name}の天気予報 ({current_time.strftime('%Y/%m/%d %H:%M')}):"]
        
        # 現在の天気を最初に表示
        if len(times) > 0:
            # 現在の時刻に最も近いデータを探す
            current_hour = current_time.hour
            closest_index = 0
            for i in range(len(times)):
                dt = datetime.fromisoformat(times[i].replace('T', ' '))
                if dt.hour >= current_hour:
                    closest_index = i
                    break
            
            # 現在の天気
            temp = temperatures[closest_index]
            precip_prob = precipitation_probs[closest_index] if precipitation_probs[closest_index] is not None else 0
            weather_code = weather_codes[closest_index]
            wind_speed = wind_speeds[closest_index] if wind_speeds[closest_index] is not None else 0
            humidity = humidities[closest_index] if humidities[closest_index] is not None else 0
            weather_desc = convert_wmo_code(weather_code)
            
            result_lines.append(f"現在の天気: {weather_desc}")
            result_lines.append(f"気温: {temp}°C")
            result_lines.append(f"降水確率: {precip_prob}%")
            result_lines.append(f"風速: {wind_speed}m/s")
            result_lines.append(f"湿度: {humidity}%")
            result_lines.append("")  # 空行
            result_lines.append("--- 3時間ごとの予報 ---")
        
        # 3時間ごとのデータを処理（24時間分 = 8データポイント）
        for i in range(0, min(24, len(times)), 3):
            time_str = times[i]
            temp = temperatures[i]
            precip_prob = precipitation_probs[i] if precipitation_probs[i] is not None else 0
            weather_code = weather_codes[i]
            wind_speed = wind_speeds[i] if wind_speeds[i] is not None else 0
            humidity = humidities[i] if humidities[i] is not None else 0
            
            # 時刻フォーマット変換
            dt = datetime.fromisoformat(time_str.replace('T', ' '))
            time_formatted = dt.strftime('%H時')
            
            # 天気説明
            weather_desc = convert_wmo_code(weather_code)
            
            # 1行にまとめて表示（簡潔に）
            line = f"{time_formatted}: {weather_desc} {temp}°C 降水{precip_prob}% 風{wind_speed}m/s"
            result_lines.append(line)
        
        return "\n".join(result_lines)
        
    except KeyError as e:
        return f"天気データの解析中にエラーが発生しました。不足データ: {str(e)}"
    except Exception as e:
        return f"天気データのフォーマット中に予期しないエラーが発生しました: {str(e)}"


def get_weather_for_city(city_name: str) -> str:
    """
    都市名から完全な天気予報を取得（メイン関数）
    
    Args:
        city_name (str): 都市名または詳細住所
    
    Returns:
        str: フォーマット済み天気予報またはエラーメッセージ
    """
    # Step 1: 地名解決
    latitude, longitude, geo_error = get_coordinates(city_name)
    
    if geo_error:
        return f"エラー: {geo_error}"
    
    # Step 2: 天気データ取得
    weather_data, weather_error = get_weather_forecast(latitude, longitude)
    
    if weather_error:
        return f"エラー: {weather_error}"
    
    # Step 3: データフォーマット
    formatted_result = format_weather_data(weather_data, city_name)
    
    return formatted_result


# テスト用メイン関数
if __name__ == "__main__":
    # 基本テスト
    test_cities = ["東京都", "大阪府", "札幌市", "福岡市", "那覇市"]
    
    # 詳細住所テスト（重要）
    detailed_test_cities = ["宮崎県都城市上長飯町", "都城市上長飯町", "都城市"]
    
    print("=== 基本テスト ===")
    for city in test_cities:
        print(f"\n--- {city} ---")
        result = get_weather_for_city(city)
        print(result[:200] + "..." if len(result) > 200 else result)
    
    print("\n=== 詳細住所テスト ===")
    for city in detailed_test_cities:
        print(f"\n--- {city} ---")
        result = get_weather_for_city(city)
        print(result[:200] + "..." if len(result) > 200 else result)