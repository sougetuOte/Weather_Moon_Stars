from datetime import datetime
import math

def calculate_moon_age():
    now = datetime.now()
    new_moon_date = datetime(2000, 1, 6, 18, 14)  # 2000年1月6日18時14分（JST）が新月
    diff = now - new_moon_date
    moon_age = (diff.total_seconds() / (24 * 60 * 60)) % 29.53058867  # 月齢を計算
    return round(moon_age, 2)
