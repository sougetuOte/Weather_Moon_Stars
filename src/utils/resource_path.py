"""
リソースファイルのパス解決ユーティリティ

PyInstallerでexe化された場合とソース実行時の両方で正しく動作するようにパスを解決します。
"""

import sys
import os


def get_resource_path(relative_path):
    """
    リソースファイルの絶対パスを取得
    
    Args:
        relative_path: リソースファイルの相対パス
        
    Returns:
        リソースファイルの絶対パス
    """
    # PyInstallerでexe化された場合
    if hasattr(sys, '_MEIPASS'):
        # _MEIPASSは、PyInstallerが一時的に展開したファイルのパス
        base_path = sys._MEIPASS
    else:
        # 通常のPython実行時
        # このファイルから2階層上がプロジェクトルート（src/utils/resource_path.py）
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)


def get_data_file_path(filename):
    """
    dataディレクトリ内のファイルパスを取得
    
    Args:
        filename: dataディレクトリ内のファイル名
        
    Returns:
        ファイルの絶対パス
    """
    return get_resource_path(os.path.join('data', filename))


def get_config_file_path(filename):
    """
    configディレクトリ内のファイルパスを取得
    
    Args:
        filename: configディレクトリ内のファイル名
        
    Returns:
        ファイルの絶対パス
    """
    # exe化時はconfigファイルも同梱される想定
    return get_resource_path(os.path.join('config', filename))


# 便利な定数
ASTROLOGY_DATA_PATH = get_data_file_path('astrology_data.json')