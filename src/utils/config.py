import configparser

class AppConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config/app_config.ini', encoding='utf-8')

    def get(self, section, option):
        if self.config.has_section(section) and self.config.has_option(section, option):
            return self.config.get(section, option)
        else:
            return None

    def set(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        with open('config/app_config.ini', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        

# グローバル設定オブジェクトの作成
app_config = AppConfig()