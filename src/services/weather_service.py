"""
天気サービス実装

既存のopen_meteo_api.pyをラップし、データモデルに変換するサービス層
"""
import sys
import os
from datetime import datetime
from typing import List, Optional
import re

# パスを追加して既存モジュールをインポート可能に
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.data_models import WeatherData, HourlyForecast
from services.interfaces import IWeatherService, WeatherServiceError


class WeatherService(IWeatherService):
    """天気サービス実装（既存APIのラッパー）"""
    
    def __init__(self):
        """サービスの初期化"""
        self._city_pattern = re.compile(
            r'^[a-zA-Z0-9\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF'
            r'\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F'
            r'\u2B820-\u2CEAF\u2CEB0-\u2EBEF\u30000-\u3134F\-]+$'
        )
    
    def get_weather_sync(self, city_name: str) -> WeatherData:
        """
        同期的に天気情報を取得（移行期間用）
        
        Phase 1では既存のAPIをラップして、段階的な移行を実現
        """
        try:
            # 既存のAPIをインポート
            from api.open_meteo_api import get_weather_for_city
            
            # 既存の関数を呼び出し
            raw_result = get_weather_for_city(city_name)
            
            # エラーチェック
            if raw_result.startswith("エラー:"):
                raise WeatherServiceError(raw_result)
            
            # WeatherDataモデルに変換
            return self._parse_to_weather_data(raw_result, city_name)
            
        except ImportError as e:
            raise WeatherServiceError(f"APIモジュールの読み込みに失敗: {str(e)}")
        except Exception as e:
            if isinstance(e, WeatherServiceError):
                raise
            raise WeatherServiceError(f"天気情報の取得中にエラーが発生: {str(e)}")
    
    def validate_city_name(self, city_name: str) -> bool:
        """
        都市名の妥当性チェック
        
        日本語、英数字、スペース、ハイフンのみ許可
        """
        if not city_name or not city_name.strip():
            return False
        
        return bool(self._city_pattern.match(city_name.strip()))
    
    def _parse_to_weather_data(self, raw_result: str, city_name: str) -> WeatherData:
        """
        既存のテキスト形式をデータモデルに変換
        
        既存のformat_weather_dataの出力形式をパースして
        構造化されたWeatherDataオブジェクトに変換
        """
        lines = raw_result.strip().split('\n')
        
        # デフォルト値の設定
        current_temp = 0.0
        current_weather = "不明"
        humidity = 0
        wind_speed = 0.0
        precipitation_prob = 0
        hourly_forecast = []
        
        # 現在の天気情報をパース
        parsing_current = False
        parsing_forecast = False
        
        for line in lines:
            line = line.strip()
            
            # 現在の天気セクション
            if "現在の天気:" in line:
                current_weather = line.split("現在の天気:")[-1].strip()
                parsing_current = True
                continue
            
            if parsing_current:
                if "気温:" in line:
                    temp_str = line.split("気温:")[-1].replace("°C", "").strip()
                    try:
                        current_temp = float(temp_str)
                    except ValueError:
                        pass
                elif "降水確率:" in line:
                    prob_str = line.split("降水確率:")[-1].replace("%", "").strip()
                    try:
                        precipitation_prob = int(prob_str)
                    except ValueError:
                        pass
                elif "風速:" in line:
                    wind_str = line.split("風速:")[-1].replace("m/s", "").strip()
                    try:
                        wind_speed = float(wind_str)
                    except ValueError:
                        pass
                elif "湿度:" in line:
                    hum_str = line.split("湿度:")[-1].replace("%", "").strip()
                    try:
                        humidity = int(hum_str)
                    except ValueError:
                        pass
            
            # 予報セクション
            if "--- 3時間ごとの予報 ---" in line:
                parsing_current = False
                parsing_forecast = True
                continue
            
            if parsing_forecast and "時:" in line:
                # 形式: "15時: 曇り 23.0°C 降水0% 風2.0m/s"
                parts = line.split(":")
                if len(parts) >= 2:
                    time_str = parts[0].strip()
                    info_parts = parts[1].strip().split()
                    
                    if len(info_parts) >= 4:
                        try:
                            # 時刻を現在の日付と組み合わせてdatetimeに
                            hour = int(time_str.replace("時", ""))
                            forecast_time = datetime.now().replace(
                                hour=hour, minute=0, second=0, microsecond=0
                            )
                            
                            # 天気説明
                            weather_desc = info_parts[0]
                            
                            # 気温
                            temp = float(info_parts[1].replace("°C", ""))
                            
                            # 降水確率
                            precip = int(info_parts[2].replace("降水", "").replace("%", ""))
                            
                            # 風速
                            wind = float(info_parts[3].replace("風", "").replace("m/s", ""))
                            
                            # HourlyForecastオブジェクトを作成
                            forecast = HourlyForecast(
                                time=forecast_time,
                                temperature=temp,
                                weather_description=weather_desc,
                                precipitation_probability=precip,
                                wind_speed=wind,
                                humidity=humidity  # 現在の湿度を使用（簡易実装）
                            )
                            hourly_forecast.append(forecast)
                            
                        except (ValueError, IndexError):
                            # パースエラーは無視して続行
                            pass
        
        # WeatherDataオブジェクトを作成
        return WeatherData(
            city_name=city_name,
            current_temp=current_temp,
            current_weather=current_weather,
            humidity=humidity,
            wind_speed=wind_speed,
            precipitation_prob=precipitation_prob,
            hourly_forecast=hourly_forecast
        )