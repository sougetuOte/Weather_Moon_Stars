import json
from utils.config import app_config
from utils.resource_path import get_data_file_path
import ephem

# 星座データを読み込む
def load_astrology_data():
    try:
        astrology_data_file = app_config.get('Astrology','ASTROLOGY_DATA_FILE')
        if astrology_data_file is None:
            # デフォルト値を使用
            astrology_data_file = 'astrology_data.json'
            print("設定ファイルから星座データファイル名を取得できませんでした。デフォルト値を使用します。")
        
        # exe化対応のパス解決
        file_path = get_data_file_path(astrology_data_file)
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # エラーログ出力とデフォルトデータ返却
        print(f"設定ファイル読み込みエラー: {e}")
        print("デフォルトの星座データを使用します。")
        # 最低限のデフォルトデータ
        return {
            "signs": [
                {"name": "おひつじ座", "start_age": 0, "end_age": 30, "description": "新しい始まりの時期"},
                {"name": "おうし座", "start_age": 30, "end_age": 60, "description": "安定と豊かさの時期"},
                {"name": "ふたご座", "start_age": 60, "end_age": 90, "description": "コミュニケーションの時期"},
                {"name": "かに座", "start_age": 90, "end_age": 120, "description": "感情と家庭の時期"},
                {"name": "しし座", "start_age": 120, "end_age": 150, "description": "創造性と表現の時期"},
                {"name": "おとめ座", "start_age": 150, "end_age": 180, "description": "分析と完璧性の時期"},
                {"name": "てんびん座", "start_age": 180, "end_age": 210, "description": "バランスと調和の時期"},
                {"name": "さそり座", "start_age": 210, "end_age": 240, "description": "変容と深化の時期"},
                {"name": "いて座", "start_age": 240, "end_age": 270, "description": "探求と学習の時期"},
                {"name": "やぎ座", "start_age": 270, "end_age": 300, "description": "責任と達成の時期"},
                {"name": "みずがめ座", "start_age": 300, "end_age": 330, "description": "革新と友情の時期"},
                {"name": "うお座", "start_age": 330, "end_age": 360, "description": "直感と慈悲の時期"}
            ]
        }

# 月星座の計算
def get_moon_sign(date=None):
    if date is None:
        date = ephem.now()
    moon = ephem.Moon(date)
    ecliptic_lon = ephem.Ecliptic(moon).lon
    sign, description = determine_sign(ecliptic_lon)
    return sign, description

def determine_sign(longitude):
    # 黄道座標の経度（ラジアン）を度に変換
    long_deg = float(longitude) * 180.0 / ephem.pi
    astrology_data = load_astrology_data()
    
    for sign in astrology_data["signs"]:
        if sign["start_age"] <= long_deg < sign["end_age"]:
            return sign["name"], sign["description"]
    
    # 万が一のためのデフォルト値
    return "不明", "星座の情報が見つかりませんでした。"

# 現在の月星座とその解説を取得する例
sign, description = get_moon_sign()
# print(f"月星座: {sign}, 解説: {description}\n")
