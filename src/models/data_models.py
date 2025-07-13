"""
データモデル定義

天気情報と天体情報を扱うための型安全なデータモデル
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class HourlyForecast:
    """時間ごとの予報データ"""
    time: datetime
    temperature: float
    weather_description: str
    precipitation_probability: int
    wind_speed: float
    humidity: int


@dataclass
class WeatherData:
    """天気データモデル"""
    city_name: str
    current_temp: float
    current_weather: str
    humidity: int
    wind_speed: float
    precipitation_prob: int
    hourly_forecast: List[HourlyForecast]
    
    def get_forecast_for_hours(self, hours: int = 24) -> List[HourlyForecast]:
        """指定時間分の予報を取得"""
        return self.hourly_forecast[:hours]
    
    def get_forecast_every_n_hours(self, n: int = 3) -> List[HourlyForecast]:
        """n時間ごとの予報を取得（デフォルト3時間）"""
        return self.hourly_forecast[::n]


@dataclass
class AstronomyData:
    """天体情報データモデル"""
    moon_age: float
    moon_phase_name: str
    moon_zodiac: str
    zodiac_description: str
    
    def format_moon_age(self) -> str:
        """月齢を小数点第2位までフォーマット"""
        return f"{self.moon_age:.2f}"