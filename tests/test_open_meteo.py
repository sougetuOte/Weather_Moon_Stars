#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Open-Meteo API テストスクリプト
都城市上長飯町を含む詳細住所テストを実行
"""

import sys
import os
import time
from datetime import datetime

# srcパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_libraries():
    """必要なライブラリの確認"""
    print("=== ライブラリ確認 ===")
    try:
        import geopy
        print(f"✅ geopy version: {geopy.__version__}")
    except ImportError as e:
        print(f"❌ geopy import failed: {e}")
        return False
    
    try:
        import requests
        print(f"✅ requests version: {requests.__version__}")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        import ephem
        print(f"✅ ephem version: {ephem.__version__}")
    except ImportError as e:
        print(f"❌ ephem import failed: {e}")
        return False
    
    return True

def test_detailed_addresses():
    """詳細住所テスト（最重要）"""
    print("\n=== 詳細住所テスト ===")
    
    try:
        from api.open_meteo_api import get_weather_for_city
        
        test_locations = [
            "宮崎県都城市上長飯町",  # ユーザー実住所
            "都城市上長飯町",        # 略記版
            "都城市",               # 比較用
        ]
        
        for location in test_locations:
            print(f"\n--- {location} ---")
            start_time = time.time()
            
            try:
                result = get_weather_for_city(location)
                elapsed_time = time.time() - start_time
                
                print(f"⏱️ 実行時間: {elapsed_time:.2f}秒")
                
                if "エラー" in result:
                    print(f"❌ エラー発生: {result[:100]}...")
                else:
                    print(f"✅ 成功: {result[:100]}...")
                    
            except Exception as e:
                elapsed_time = time.time() - start_time
                print(f"❌ 例外発生 ({elapsed_time:.2f}秒): {str(e)}")
                
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("open_meteo_api.py が見つからないか、実装に問題があります")

def test_basic_cities():
    """基本5都市テスト"""
    print("\n=== 基本5都市テスト ===")
    
    try:
        from api.open_meteo_api import get_weather_for_city
        
        basic_cities = ["東京都", "大阪府", "札幌市", "福岡市", "那覇市"]
        
        for city in basic_cities:
            print(f"\n--- {city} ---")
            start_time = time.time()
            
            try:
                result = get_weather_for_city(city)
                elapsed_time = time.time() - start_time
                
                print(f"⏱️ 実行時間: {elapsed_time:.2f}秒")
                
                if "エラー" in result:
                    print(f"❌ エラー: {result[:100]}...")
                else:
                    print(f"✅ 成功: {result[:100]}...")
                    
            except Exception as e:
                elapsed_time = time.time() - start_time
                print(f"❌ 例外 ({elapsed_time:.2f}秒): {str(e)}")
                
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")

def test_error_cases():
    """エラーケーステスト"""
    print("\n=== エラーケーステスト ===")
    
    try:
        from api.open_meteo_api import get_weather_for_city
        
        error_cases = [
            "存在しない都市名",
            "",  # 空文字列
            "!@#$%",  # 特殊文字
            "New York",  # 海外都市
        ]
        
        for test_case in error_cases:
            print(f"\n--- '{test_case}' ---")
            
            try:
                result = get_weather_for_city(test_case)
                
                if "エラー" in result:
                    print(f"✅ 適切なエラー: {result[:100]}...")
                else:
                    print(f"⚠️ エラーが期待されたが成功: {result[:100]}...")
                    
            except Exception as e:
                print(f"❌ 予期しない例外: {str(e)}")
                
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")

def main():
    """メイン実行関数"""
    print("Open-Meteo API テスト開始")
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # ライブラリ確認
    if not test_libraries():
        print("❌ ライブラリ確認に失敗しました。")
        return
    
    # 詳細住所テスト（最重要）
    test_detailed_addresses()
    
    # 基本都市テスト
    test_basic_cities()
    
    # エラーケーステスト
    test_error_cases()
    
    print("\n" + "=" * 50)
    print("✅ テスト完了")

if __name__ == "__main__":
    main()