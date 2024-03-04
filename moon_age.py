from datetime import datetime
import ephem

# 月齢を計算する関数
def get_moon_age(date=None):
    if date is None:
        date = datetime.utcnow()
    observer = ephem.Observer()
    observer.date = date.strftime('%Y/%m/%d')
    # 最後の新月の日時を取得
    last_new_moon = ephem.previous_new_moon(observer.date)
    # 指定された日付と最後の新月の日時の差を計算
    moon_age = observer.date - last_new_moon
    # 月齢を日数で返す
    return moon_age

# print(get_moon_age())