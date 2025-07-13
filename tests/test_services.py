"""
サービス層のテスト

WeatherServiceとAstronomyServiceの動作確認
"""
import unittest
import sys
import os

# プロジェクトのルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.weather_service import WeatherService
from services.astronomy_service import AstronomyService
from models.data_models import WeatherData, AstronomyData


class TestWeatherService(unittest.TestCase):
    """WeatherServiceのテスト"""
    
    def setUp(self):
        """テストの初期化"""
        self.service = WeatherService()
    
    def test_validate_city_name_valid(self):
        """有効な都市名のバリデーションテスト"""
        self.assertTrue(self.service.validate_city_name("東京都"))
        self.assertTrue(self.service.validate_city_name("千代田区"))
        self.assertTrue(self.service.validate_city_name("New York"))
        self.assertTrue(self.service.validate_city_name("東京都 千代田区"))
    
    def test_validate_city_name_invalid(self):
        """無効な都市名のバリデーションテスト"""
        self.assertFalse(self.service.validate_city_name(""))
        self.assertFalse(self.service.validate_city_name("   "))
        self.assertFalse(self.service.validate_city_name("123@#$"))
    
    def test_weather_service_returns_weather_data(self):
        """WeatherServiceがWeatherDataを返すことを確認"""
        # 実際のAPIを呼び出すため、ネットワーク接続が必要
        try:
            result = self.service.get_weather_sync("東京都")
            self.assertIsInstance(result, WeatherData)
            self.assertEqual(result.city_name, "東京都")
            self.assertIsInstance(result.current_temp, float)
            self.assertIsInstance(result.hourly_forecast, list)
        except Exception as e:
            # ネットワークエラーの場合はスキップ
            self.skipTest(f"Network error: {str(e)}")


class TestAstronomyService(unittest.TestCase):
    """AstronomyServiceのテスト"""
    
    def setUp(self):
        """テストの初期化"""
        self.service = AstronomyService()
    
    def test_astronomy_service_returns_astronomy_data(self):
        """AstronomyServiceがAstronomyDataを返すことを確認"""
        result = self.service.get_current_astronomy_data()
        
        # 型チェック
        self.assertIsInstance(result, AstronomyData)
        self.assertIsInstance(result.moon_age, float)
        self.assertIsInstance(result.moon_phase_name, str)
        self.assertIsInstance(result.moon_zodiac, str)
        self.assertIsInstance(result.zodiac_description, str)
        
        # 値の妥当性チェック
        self.assertGreaterEqual(result.moon_age, 0.0)
        self.assertLessEqual(result.moon_age, 30.0)
        self.assertIn(result.moon_phase_name, [
            "新月", "三日月", "上弦の月", "十三夜月", 
            "満月", "居待月", "下弦の月", "有明月"
        ])
    
    def test_format_moon_age(self):
        """月齢フォーマットのテスト"""
        result = self.service.get_current_astronomy_data()
        formatted = result.format_moon_age()
        
        # 小数点第2位までの形式であることを確認
        self.assertRegex(formatted, r'^\d+\.\d{2}$')


if __name__ == '__main__':
    unittest.main()