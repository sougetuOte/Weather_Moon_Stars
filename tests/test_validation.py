#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
改善されたバリデーションテスト
"""

import sys
import os

# srcパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_improved_validation():
    """改善されたバリデーションテスト"""
    print("=== 改善されたバリデーションテスト ===")
    
    try:
        from api.open_meteo_api import get_weather_for_city
        
        test_cases = [
            ("", "空文字列"),
            ("   ", "スペースのみ"),
            ("!@#$%", "特殊文字"),
            ("Tokyo", "英語都市名"),
            ("東京都", "正常なケース"),
        ]
        
        for city, desc in test_cases:
            print(f'\n{desc}: "{city}"')
            try:
                result = get_weather_for_city(city)
                if "エラー" in result:
                    print(f"✅ 適切なエラー: {result[:80]}...")
                else:
                    print(f"⚠️ 成功: {result[:80]}...")
            except Exception as e:
                print(f"❌ 例外: {str(e)}")
                
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")

if __name__ == "__main__":
    test_improved_validation()