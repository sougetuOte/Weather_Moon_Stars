import json
from utils.config import app_config
import ephem

# 星座データを読み込む
def load_astrology_data():
    astrology_data_file = app_config.get('Astrology','ASTROLOGY_DATA_FILE')
    with open(f"data/{astrology_data_file}", "r", encoding="utf-8") as f:
        return json.load(f)

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
