import os
import json
from config import ASTROLOGY_DATA_FILE_PATH
from moon_age import calculate_moon_age

def load_astrology_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

ASTROLOGY_DATA = load_astrology_data(ASTROLOGY_DATA_FILE_PATH)

def get_moon_astrology():
    moon_age = calculate_moon_age()
    moon_astrology = None
    for sign in ASTROLOGY_DATA["signs"]:
        if sign["start_age"] <= moon_age <= sign["end_age"]:
            moon_astrology = sign
            break

    if moon_astrology:
        return moon_astrology["name"], moon_astrology["description"]
    else:
        return "不明", "月星座が見つかりませんでした。"
