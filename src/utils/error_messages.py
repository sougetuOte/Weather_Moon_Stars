"""
エラーメッセージ管理モジュール

統一されたエラーメッセージの提供と、ユーザーフレンドリーなメッセージへの変換を行います。
将来の多言語対応も考慮した設計になっています。
"""

from typing import Dict, Optional
import re

class ErrorMessageManager:
    """エラーメッセージの統一管理クラス"""
    
    # エラータイプとユーザー向けメッセージのマッピング
    ERROR_MESSAGES: Dict[str, str] = {
        # ネットワーク関連
        'network_timeout': '接続がタイムアウトしました。インターネット接続を確認してください。',
        'network_connection': 'ネットワークに接続できません。インターネット接続を確認してください。',
        'network_dns': '指定されたサーバーが見つかりません。しばらく待ってから再度お試しください。',
        
        # API関連
        'api_rate_limit': 'APIの利用制限に達しました。しばらく待ってから再度お試しください。',
        'api_invalid_response': '天気情報の取得に失敗しました。しばらく待ってから再度お試しください。',
        'api_service_unavailable': '天気予報サービスが一時的に利用できません。',
        
        # 入力関連
        'city_not_found': '指定された都市が見つかりませんでした。都市名を確認してください。',
        'invalid_input': '入力内容が正しくありません。もう一度確認してください。',
        
        # システム関連
        'file_not_found': '必要なファイルが見つかりません。アプリケーションを再インストールしてください。',
        'permission_denied': 'ファイルへのアクセス権限がありません。',
        'unknown_error': '予期しないエラーが発生しました。アプリケーションを再起動してください。',
    }
    
    # エラーメッセージパターンマッチング
    ERROR_PATTERNS = [
        (r'timeout|timed out', 'network_timeout'),
        (r'connection|connect', 'network_connection'),
        (r'name resolution|dns|getaddrinfo', 'network_dns'),
        (r'rate limit|too many requests|429', 'api_rate_limit'),
        (r'invalid response|json|decode', 'api_invalid_response'),
        (r'service unavailable|503|500', 'api_service_unavailable'),
        (r'city not found|location not found|not found', 'city_not_found'),
        (r'file not found|no such file', 'file_not_found'),
        (r'permission denied|access denied', 'permission_denied'),
    ]
    
    @classmethod
    def get_user_friendly_message(cls, error: Exception) -> str:
        """
        例外オブジェクトからユーザーフレンドリーなメッセージを生成
        
        Args:
            error: 発生した例外
            
        Returns:
            ユーザー向けのエラーメッセージ
        """
        error_str = str(error).lower()
        
        # パターンマッチングでエラータイプを特定
        for pattern, error_type in cls.ERROR_PATTERNS:
            if re.search(pattern, error_str, re.IGNORECASE):
                return cls.ERROR_MESSAGES.get(error_type, cls.ERROR_MESSAGES['unknown_error'])
        
        # デフォルトメッセージ
        return cls.ERROR_MESSAGES['unknown_error']
    
    @classmethod
    def get_message(cls, error_type: str) -> str:
        """
        エラータイプから直接メッセージを取得
        
        Args:
            error_type: エラーの種類を示すキー
            
        Returns:
            対応するエラーメッセージ
        """
        return cls.ERROR_MESSAGES.get(error_type, cls.ERROR_MESSAGES['unknown_error'])
    
    @classmethod
    def format_error_with_details(cls, error: Exception, include_technical: bool = False) -> str:
        """
        詳細情報を含むエラーメッセージをフォーマット
        
        Args:
            error: 発生した例外
            include_technical: 技術的な詳細を含めるかどうか
            
        Returns:
            フォーマットされたエラーメッセージ
        """
        user_message = cls.get_user_friendly_message(error)
        
        if include_technical and str(error):
            # 技術的な詳細を追加（開発者向け）
            return f"{user_message}\n\n[詳細情報: {type(error).__name__}: {str(error)}]"
        
        return user_message


# 便利な関数
def get_user_friendly_error(error: Exception) -> str:
    """エラーをユーザーフレンドリーなメッセージに変換"""
    return ErrorMessageManager.get_user_friendly_message(error)