"""
サービス層のインターフェース定義

ビジネスロジックの抽象化と疎結合化のためのインターフェース
"""
from abc import ABC, abstractmethod
from typing import Optional
from models.data_models import WeatherData, AstronomyData


class IWeatherService(ABC):
    """天気サービスインターフェース"""
    
    @abstractmethod
    def get_weather_sync(self, city_name: str) -> WeatherData:
        """
        同期的に天気情報を取得
        
        Args:
            city_name: 都市名または詳細住所
            
        Returns:
            WeatherData: 天気データモデル
            
        Raises:
            WeatherServiceError: 天気情報取得失敗時
        """
        pass
    
    @abstractmethod
    def validate_city_name(self, city_name: str) -> bool:
        """
        都市名の妥当性チェック
        
        Args:
            city_name: 検証する都市名
            
        Returns:
            bool: 妥当な場合True
        """
        pass


class IAstronomyService(ABC):
    """天体情報サービスインターフェース"""
    
    @abstractmethod
    def get_current_astronomy_data(self) -> AstronomyData:
        """
        現在の天体情報を取得
        
        Returns:
            AstronomyData: 天体情報データモデル
        """
        pass


class WeatherServiceError(Exception):
    """天気サービスのエラー"""
    pass


class AstronomyServiceError(Exception):
    """天体サービスのエラー"""
    pass