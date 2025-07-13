"""
アプリケーション設定管理

既存のapp_configをラップし、より使いやすく拡張可能な設定管理を提供します。
将来の拡張（環境変数、JSONファイル、デフォルト値管理など）に備えた構造です。
"""

from typing import Any, Optional, Dict
from utils.config import app_config
import os
import json


class AppSettings:
    """アプリケーション設定の統一管理クラス"""
    
    # デフォルト設定値
    DEFAULT_SETTINGS = {
        'LastSearch': {
            'CITY_NAME': '東京都'
        },
        'Display': {
            'THEME': 'light',
            'FONT_SIZE': 10
        },
        'API': {
            'TIMEOUT': 5,
            'RETRY_COUNT': 3
        }
    }
    
    def __init__(self):
        self._config = app_config
        self._cache: Dict[str, Any] = {}
        
    def get(self, section: str, key: str, default: Optional[Any] = None) -> Any:
        """
        設定値を取得
        
        Args:
            section: セクション名
            key: キー名
            default: デフォルト値（指定がない場合はDEFAULT_SETTINGSから取得）
            
        Returns:
            設定値
        """
        # キャッシュを確認
        cache_key = f"{section}.{key}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # 既存のapp_configから取得を試みる
        try:
            value = self._config.get(section, key)
            if value is not None:
                self._cache[cache_key] = value
                return value
        except:
            pass
        
        # デフォルト値を返す
        if default is not None:
            return default
        
        # DEFAULT_SETTINGSから取得
        if section in self.DEFAULT_SETTINGS and key in self.DEFAULT_SETTINGS[section]:
            return self.DEFAULT_SETTINGS[section][key]
        
        return None
    
    def set(self, section: str, key: str, value: Any) -> bool:
        """
        設定値を保存
        
        Args:
            section: セクション名
            key: キー名
            value: 設定値
            
        Returns:
            保存の成功/失敗
        """
        try:
            # キャッシュを更新
            cache_key = f"{section}.{key}"
            self._cache[cache_key] = value
            
            # 既存のapp_configに保存
            self._config.set(section, key, value)
            return True
        except Exception as e:
            print(f"設定の保存に失敗しました: {e}")
            return False
    
    def get_last_city(self) -> str:
        """最後に検索した都市名を取得（便利メソッド）"""
        return self.get('LastSearch', 'CITY_NAME', '東京都')
    
    def set_last_city(self, city_name: str) -> bool:
        """最後に検索した都市名を保存（便利メソッド）"""
        return self.set('LastSearch', 'CITY_NAME', city_name)
    
    def get_api_timeout(self) -> int:
        """APIタイムアウト時間を取得"""
        return self.get('API', 'TIMEOUT', 5)
    
    def is_debug_mode(self) -> bool:
        """デバッグモードかどうかを確認"""
        return os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    def is_new_service_enabled(self) -> bool:
        """新サービスが有効かどうかを確認"""
        return os.getenv('USE_NEW_SERVICE', 'false').lower() == 'true'
    
    def clear_cache(self):
        """設定キャッシュをクリア"""
        self._cache.clear()
    
    def export_settings(self, filepath: str) -> bool:
        """
        設定をJSONファイルにエクスポート（将来の拡張用）
        
        Args:
            filepath: 出力先ファイルパス
            
        Returns:
            エクスポートの成功/失敗
        """
        try:
            # 現在の設定を収集
            settings = {}
            for section in self.DEFAULT_SETTINGS:
                settings[section] = {}
                for key in self.DEFAULT_SETTINGS[section]:
                    value = self.get(section, key)
                    if value is not None:
                        settings[section][key] = value
            
            # JSONファイルに保存
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"設定のエクスポートに失敗しました: {e}")
            return False


# シングルトンインスタンス
app_settings = AppSettings()


# 便利な関数
def get_setting(section: str, key: str, default: Optional[Any] = None) -> Any:
    """設定値を取得"""
    return app_settings.get(section, key, default)


def set_setting(section: str, key: str, value: Any) -> bool:
    """設定値を保存"""
    return app_settings.set(section, key, value)