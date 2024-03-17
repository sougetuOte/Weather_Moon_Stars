from skyfield.api import load, Star, load_file
from skyfield.framelib import ecliptic_frame
from datetime import datetime, timedelta

# 天体の位置を計算するための関数
def calculate_position(date, body):
    # Skyfieldのデータファイルをダウンロード
    eph = load('de421.bsp')

    # 天体の位置を計算
    if body == "Moon":
        target = eph['moon']
    elif body == "Sun":
        target = eph['sun']
    else:
        raise ValueError("Invalid body specified.")

    # 指定された日時のSkyfieldのTime objectを作成
    t = load.timescale().utc(date.year, date.month, date.day, date.hour, date.minute, date.second)

    # 天体の位置を計算
    position = target.at(t)

    # 黄道座標系に変換
    ecliptic_position = position.frame_latlon(ecliptic_frame)

    # 黄経を取得
    longitude = ecliptic_position.longitude.degrees

    return longitude

# VoidTimeを判定する関数
def is_void_time(date):
    # 月と太陽の黄経を計算
    moon_longitude = calculate_position(date, "Moon")
    sun_longitude = calculate_position(date, "Sun")

    # VoidTimeの判定条件を確認
    if moon_longitude > sun_longitude:
        return True
    else:
        return False

# 現在の日付と時刻を取得
now = datetime.now()

# VoidTimeを判定
if is_void_time(now):
    print("現在はVoidTimeです。")
else:
    print("現在はVoidTimeではありません。")

# VoidTimeの開始時刻と終了時刻を探索
start_time = None
end_time = None
time_step = timedelta(minutes=1)  # 1分単位で探索

# 現在時刻から48時間先までを探索
for i in range(48 * 60):
    current_time = now + i * time_step
    if is_void_time(current_time):
        if start_time is None:
            start_time = current_time
        end_time = current_time
    else:
        if start_time is not None:
            break

# VoidTimeの情報を出力
if start_time is not None and end_time is not None:
    void_duration = end_time - start_time
    print(f"開始時刻: {start_time}")
    print(f"終了時刻: {end_time}")
    print(f"期間: {void_duration}")
    

