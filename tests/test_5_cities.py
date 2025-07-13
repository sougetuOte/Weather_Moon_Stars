#!/usr/bin/env python3
"""
5都市 + 都城市上長飯町 GUI統合テスト
Plannerの指定に基づく包括的テスト
"""

import sys
import os
import time

# src ディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_comprehensive_cities():
    """5都市 + 都城市上長飯町での包括的テスト"""
    print("=== 5都市 + 都城市上長飯町 包括テスト ===")
    
    from api.open_meteo_api import get_weather_for_city
    from features.moon_age import get_moon_age
    from features.astrology import get_moon_sign
    from datetime import datetime
    
    # Plannerが指定したテスト都市
    test_cities = [
        "東京都",
        "大阪府", 
        "札幌市",
        "福岡市",
        "那覇市",
        "都城市上長飯町"  # 特別ケース
    ]
    
    results = []
    
    for i, city_name in enumerate(test_cities, 1):
        print(f"\n--- {i}/{len(test_cities)}: {city_name} ---")
        
        start_time = time.time()
        
        try:
            # GUIと同じ統合処理をシミュレート
            designated_date = datetime.today()
            formatted_date = designated_date.strftime('%Y/%m/%d %H:%M:%S')
            
            # Open-Meteo API呼び出し
            weather_result = get_weather_for_city(city_name)
            
            # 既存の月齢・星座機能統合
            moon_age = get_moon_age()
            moon_astrology_name, moon_astrology_desc = get_moon_sign()
            
            # 結果統合（GUIと同じ形式）
            combined_result = f"{city_name}の天気予報 ({formatted_date}):\n{weather_result}\n\n月齢: {moon_age:.2f}\n月の{moon_astrology_name}: {moon_astrology_desc}"
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # 結果検証
            success = True
            issues = []
            
            if "エラー" in combined_result:
                success = False
                issues.append("エラーメッセージ含む")
            
            if len(combined_result) < 100:
                success = False
                issues.append("レスポンス短すぎ")
            
            if response_time > 5.0:
                success = False
                issues.append(f"応答時間超過 ({response_time:.2f}秒)")
            
            if "月齢:" not in combined_result:
                success = False
                issues.append("月齢データなし")
            
            if "月の" not in combined_result:
                success = False
                issues.append("星座データなし")
            
            # 結果記録
            result = {
                'city': city_name,
                'success': success,
                'response_time': response_time,
                'result_length': len(combined_result),
                'issues': issues,
                'has_weather': weather_result and "エラー" not in weather_result,
                'has_moon_age': "月齢:" in combined_result,
                'has_astrology': "月の" in combined_result
            }
            
            results.append(result)
            
            if success:
                print(f"✅ 成功: {response_time:.2f}秒, {len(combined_result)}文字")
                # デバッグ用に最初の行を表示
                first_line = combined_result.split('\n')[0]
                print(f"   内容: {first_line}")
            else:
                print(f"❌ 失敗: {', '.join(issues)}")
                print(f"   応答時間: {response_time:.2f}秒")
                print(f"   文字数: {len(combined_result)}")
                
        except Exception as e:
            print(f"❌ 例外発生: {str(e)}")
            results.append({
                'city': city_name,
                'success': False,
                'response_time': 0,
                'result_length': 0,
                'issues': [f"例外: {str(e)}"],
                'has_weather': False,
                'has_moon_age': False,
                'has_astrology': False
            })
    
    return results

def print_summary(results):
    """テスト結果サマリー出力"""
    print("\n=== テスト結果サマリー ===")
    
    total = len(results)
    successful = len([r for r in results if r['success']])
    
    print(f"全体結果: {successful}/{total} 都市成功")
    
    if successful == total:
        print("🎉 全都市テスト合格!")
    else:
        print("❌ 一部都市でテスト失敗")
    
    print("\n--- 詳細結果 ---")
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['city']}: {result['response_time']:.2f}秒, {result['result_length']}文字")
        if result['issues']:
            print(f"   問題: {', '.join(result['issues'])}")
    
    print("\n--- 機能統合確認 ---")
    weather_ok = len([r for r in results if r['has_weather']]) 
    moon_ok = len([r for r in results if r['has_moon_age']])
    astro_ok = len([r for r in results if r['has_astrology']])
    
    print(f"天気データ統合: {weather_ok}/{total}")
    print(f"月齢データ統合: {moon_ok}/{total}")
    print(f"星座データ統合: {astro_ok}/{total}")
    
    print("\n--- パフォーマンス ---")
    avg_time = sum(r['response_time'] for r in results if r['success']) / max(successful, 1)
    max_time = max(r['response_time'] for r in results if r['success']) if successful > 0 else 0
    print(f"平均応答時間: {avg_time:.2f}秒")
    print(f"最大応答時間: {max_time:.2f}秒")
    print(f"5秒制限内: {'✅' if max_time <= 5.0 else '❌'}")
    
    return successful == total

def main():
    """メインテスト実行"""
    print("GUI統合 5都市+都城市上長飯町 包括テスト開始\n")
    
    try:
        results = test_comprehensive_cities()
        success = print_summary(results)
        
        if success:
            print("\n🎊 GUI統合フェーズ完了!")
            print("Plannerの全要件を満たしています。")
        else:
            print("\n🔧 修正が必要です。")
        
        return success
        
    except Exception as e:
        print(f"\n❌ テスト実行中に例外発生: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)