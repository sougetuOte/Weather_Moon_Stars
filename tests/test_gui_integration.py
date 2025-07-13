#!/usr/bin/env python3
"""
GUI統合テストスクリプト
Open-Meteo API統合の動作確認と既存機能の保持確認
"""

import sys
import os

# src ディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """必要なモジュールが正常にインポートできるかテスト"""
    print("=== インポートテスト ===")
    
    try:
        from api.open_meteo_api import get_weather_for_city
        print("✅ Open-Meteo API モジュール正常インポート")
    except ImportError as e:
        print(f"❌ Open-Meteo API インポートエラー: {e}")
        return False
    
    try:
        from features.moon_age import get_moon_age
        print("✅ 月齢計算モジュール正常インポート")
    except ImportError as e:
        print(f"❌ 月齢計算インポートエラー: {e}")
        return False
    
    try:
        from features.astrology import get_moon_sign
        print("✅ 星座情報モジュール正常インポート")
    except ImportError as e:
        print(f"❌ 星座情報インポートエラー: {e}")
        return False
    
    try:
        from utils.clipboard import copy_to_clipboard
        print("✅ クリップボードモジュール正常インポート")
    except ImportError as e:
        print(f"❌ クリップボードインポートエラー: {e}")
        return False
    
    try:
        from utils.config import app_config
        print("✅ 設定モジュール正常インポート")
    except ImportError as e:
        print(f"❌ 設定インポートエラー: {e}")
        return False
    
    return True

def test_api_functionality():
    """API機能のテスト"""
    print("\n=== API機能テスト ===")
    
    from api.open_meteo_api import get_weather_for_city
    
    # 基本的な都市でテスト
    test_cities = ["東京都", "都城市上長飯町"]
    
    for city in test_cities:
        print(f"\n--- {city} のテスト ---")
        try:
            result = get_weather_for_city(city)
            if result and "エラー" not in result:
                print(f"✅ {city}: 正常取得 (文字数: {len(result)})")
                # 結果の一部を表示（デバッグ用）
                lines = result.split('\n')
                print(f"   最初の行: {lines[0] if lines else 'N/A'}")
            else:
                print(f"❌ {city}: API エラー - {result}")
                return False
        except Exception as e:
            print(f"❌ {city}: 例外発生 - {str(e)}")
            return False
    
    return True

def test_moon_features():
    """月齢・星座機能のテスト"""
    print("\n=== 月齢・星座機能テスト ===")
    
    try:
        from features.moon_age import get_moon_age
        moon_age = get_moon_age()
        print(f"✅ 月齢計算成功: {moon_age:.2f}")
    except Exception as e:
        print(f"❌ 月齢計算エラー: {e}")
        return False
    
    try:
        from features.astrology import get_moon_sign
        moon_sign_name, moon_sign_desc = get_moon_sign()
        print(f"✅ 星座情報取得成功: 月の{moon_sign_name}")
        print(f"   説明: {moon_sign_desc[:50]}...")
    except Exception as e:
        print(f"❌ 星座情報エラー: {e}")
        return False
    
    return True

def test_error_handling():
    """エラーハンドリングのテスト"""
    print("\n=== エラーハンドリングテスト ===")
    
    from api.open_meteo_api import get_weather_for_city
    
    # 空文字列テスト
    try:
        result = get_weather_for_city("")
        if "都市名を入力してください" in result:
            print("✅ 空文字列エラー処理正常")
        else:
            print(f"❌ 空文字列エラー処理異常: {result}")
            return False
    except Exception as e:
        print(f"❌ 空文字列テスト例外: {e}")
        return False
    
    # 無効な文字列テスト
    try:
        result = get_weather_for_city("@#$%^&*")
        if "使用できます" in result or "見つかりませんでした" in result:
            print("✅ 無効文字列エラー処理正常")
        else:
            print(f"❌ 無効文字列エラー処理異常: {result}")
            return False
    except Exception as e:
        print(f"❌ 無効文字列テスト例外: {e}")
        return False
    
    return True

def test_integration():
    """統合機能テスト（GUIと同様の処理フロー）"""
    print("\n=== 統合機能テスト ===")
    
    from api.open_meteo_api import get_weather_for_city
    from features.moon_age import get_moon_age
    from features.astrology import get_moon_sign
    from datetime import datetime
    
    # GUIと同じ処理フローをシミュレート
    city_name = "東京都"
    
    try:
        # 日付取得
        designated_date = datetime.today()
        formatted_date = designated_date.strftime('%Y/%m/%d %H:%M:%S')
        
        # 天気情報取得
        weather_result = get_weather_for_city(city_name)
        
        # 月齢・星座情報取得
        moon_age = get_moon_age()
        moon_astrology_name, moon_astrology_desc = get_moon_sign()
        
        # 結果統合（GUIと同じ形式）
        combined_result = f"{city_name}の天気予報 ({formatted_date}):\n{weather_result}\n\n月齢: {moon_age:.2f}\n月の{moon_astrology_name}: {moon_astrology_desc}"
        
        print("✅ 統合処理成功")
        print(f"   結果文字数: {len(combined_result)}")
        print(f"   天気データあり: {'気温' in combined_result}")
        print(f"   月齢データあり: {'月齢:' in combined_result}")
        print(f"   星座データあり: {'月の' in combined_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 統合処理エラー: {e}")
        return False

def main():
    """メインテスト実行"""
    print("GUI統合テスト開始\n")
    
    tests = [
        ("インポート", test_imports),
        ("API機能", test_api_functionality),
        ("月齢・星座機能", test_moon_features),
        ("エラーハンドリング", test_error_handling),
        ("統合機能", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name}テスト: PASS")
            else:
                print(f"\n❌ {test_name}テスト: FAIL")
        except Exception as e:
            print(f"\n❌ {test_name}テスト: EXCEPTION - {e}")
    
    print(f"\n=== テスト結果 ===")
    print(f"成功: {passed}/{total}")
    
    if passed == total:
        print("🎉 全テスト合格! GUI統合は正常に動作します。")
        return True
    else:
        print("❌ 一部テスト失敗。修正が必要です。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)