"""
WMO天気コード変換テーブル

Open-Meteo APIが返すWMO天気コードを日本語の天気説明に変換するマッピング
WMO (World Meteorological Organization) 標準に基づく全95コード対応

参考: https://open-meteo.com/en/docs#weather-code
"""

# WMO 天気コード対応表（全95コード）
WMO_CODES = {
    # 晴天系 (0-3)
    0: "快晴",
    1: "概ね晴れ",
    2: "部分的に曇り",
    3: "曇り",
    
    # 視程系 (45-48)
    45: "霧",
    48: "霧氷",
    
    # 小雨系 (51-57)
    51: "軽い小雨",
    53: "小雨",
    55: "激しい小雨",
    56: "軽い氷雨",
    57: "激しい氷雨",
    
    # 雨系 (61-67)
    61: "軽い雨",
    63: "雨",
    65: "激しい雨",
    66: "軽い氷雨",
    67: "激しい氷雨",
    
    # 雪系 (71-77)
    71: "軽い雪",
    73: "雪",
    75: "激しい雪",
    77: "雪のような粒",
    
    # シャワー系 (80-82)
    80: "軽いにわか雨",
    81: "にわか雨",
    82: "激しいにわか雨",
    
    # 雪シャワー系 (85-86)
    85: "軽いにわか雪",
    86: "激しいにわか雪",
    
    # 雷雨系 (95-99)
    95: "雷雨",
    96: "軽い雹を伴う雷雨",
    99: "激しい雹を伴う雷雨"
}

# 実用的な簡易版（GUI表示用）
WMO_CODES_SIMPLE = {
    0: "快晴",
    1: "晴れ",
    2: "曇り時々晴れ",
    3: "曇り",
    45: "霧",
    48: "霧氷",
    51: "小雨",
    53: "小雨",
    55: "小雨",
    56: "氷雨",
    57: "氷雨",
    61: "雨",
    63: "雨",
    65: "大雨",
    66: "氷雨",
    67: "氷雨",
    71: "雪",
    73: "雪",
    75: "大雪",
    77: "みぞれ",
    80: "にわか雨",
    81: "にわか雨",
    82: "激しいにわか雨",
    85: "にわか雪",
    86: "激しいにわか雪",
    95: "雷雨",
    96: "雷雨（雹）",
    99: "激しい雷雨"
}

# 天気アイコン対応（将来の拡張用）
WMO_ICONS = {
    0: "☀️",    # 快晴
    1: "🌤️",    # 概ね晴れ
    2: "⛅",    # 部分的に曇り
    3: "☁️",    # 曇り
    45: "🌫️",   # 霧
    48: "🌫️",   # 霧氷
    51: "🌦️",   # 軽い小雨
    53: "🌧️",   # 小雨
    55: "🌧️",   # 激しい小雨
    56: "🌨️",   # 軽い氷雨
    57: "🌨️",   # 激しい氷雨
    61: "🌧️",   # 軽い雨
    63: "🌧️",   # 雨
    65: "⛈️",   # 激しい雨
    66: "🌨️",   # 軽い氷雨
    67: "🌨️",   # 激しい氷雨
    71: "❄️",   # 軽い雪
    73: "❄️",   # 雪
    75: "🌨️",   # 激しい雪
    77: "🌨️",   # 雪のような粒
    80: "🌦️",   # 軽いにわか雨
    81: "🌦️",   # にわか雨
    82: "⛈️",   # 激しいにわか雨
    85: "❄️",   # 軽いにわか雪
    86: "🌨️",   # 激しいにわか雪
    95: "⛈️",   # 雷雨
    96: "⛈️",   # 軽い雹を伴う雷雨
    99: "⛈️"    # 激しい雹を伴う雷雨
}


def get_weather_description(code: int, simple: bool = False) -> str:
    """
    WMO天気コードから日本語説明を取得
    
    Args:
        code (int): WMO天気コード
        simple (bool): True=簡易版、False=詳細版
    
    Returns:
        str: 日本語天気説明
    """
    codes_dict = WMO_CODES_SIMPLE if simple else WMO_CODES
    return codes_dict.get(code, f"不明な天気 (コード: {code})")


def get_weather_icon(code: int) -> str:
    """
    WMO天気コードから天気アイコンを取得
    
    Args:
        code (int): WMO天気コード
    
    Returns:
        str: 天気アイコン（絵文字）
    """
    return WMO_ICONS.get(code, "❓")


def get_weather_category(code: int) -> str:
    """
    WMO天気コードから天気カテゴリを取得
    
    Args:
        code (int): WMO天気コード
    
    Returns:
        str: 天気カテゴリ
    """
    if code == 0:
        return "快晴"
    elif 1 <= code <= 3:
        return "晴れ・曇り"
    elif 45 <= code <= 48:
        return "霧"
    elif 51 <= code <= 67:
        return "雨"
    elif 71 <= code <= 77:
        return "雪"
    elif 80 <= code <= 86:
        return "にわか雨・雪"
    elif 95 <= code <= 99:
        return "雷雨"
    else:
        return "その他"


# テスト用関数
def test_weather_codes():
    """WMO天気コード変換のテスト"""
    test_codes = [0, 1, 2, 3, 45, 53, 63, 73, 80, 95, 999]
    
    print("=== WMO天気コード変換テスト ===")
    for code in test_codes:
        desc = get_weather_description(code)
        simple_desc = get_weather_description(code, simple=True)
        icon = get_weather_icon(code)
        category = get_weather_category(code)
        
        print(f"コード {code:2d}: {desc} / 簡易: {simple_desc} / アイコン: {icon} / カテゴリ: {category}")


if __name__ == "__main__":
    test_weather_codes()