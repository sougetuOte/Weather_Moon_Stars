import os
import json
from config import read_config
from moon_age import calculate_moon_age

# 星座データを読み込む
def load_astrology_data():
    _, astrology_data_file = read_config()
    with open(astrology_data_file, "r", encoding="utf-8") as f:
        return json.load(f)

# 月の星座を取得する
def get_moon_astrology():
    moon_age = calculate_moon_age()
    moon_astrology = None
    ASTROLOGY_DATA = load_astrology_data()
    for sign in ASTROLOGY_DATA["signs"]:
        if sign["start_age"] <= moon_age <= sign["end_age"]:
            moon_astrology = sign
            break

    if moon_astrology:
        return moon_astrology["name"], moon_astrology["description"]
    else:
        return "不明", "月星座が見つかりませんでした。"
