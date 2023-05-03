import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read("app_config.ini")

    api_key = config.get("OpenWeather", "API_KEY")
    astrology_data_file = config.get("Astrology", "ASTROLOGY_DATA_FILE")

    return api_key, astrology_data_file
