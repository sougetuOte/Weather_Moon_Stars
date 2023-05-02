from datetime import datetime
import math

def julian_day(date):
    y = date.year
    m = date.month
    d = date.day
    if m <= 2:
        y -= 1
        m += 12
    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + B - 1524.5


def calculate_moon_age():
    date = datetime.now()
    jd = julian_day(date)
    T = (jd - 2451550.1) / 36525
    T2 = T * T
    T3 = T2 * T
    M = 134.9634 + 477198.8675 * T + 0.0087211 * T2 + T3 / 69699 - T3 / 14712000
    M = M % 360
    M = round((M/360)*29.53058867, 2)
    return M
