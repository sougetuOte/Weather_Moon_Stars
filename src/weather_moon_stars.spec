# -*- mode: python ; coding: utf-8 -*-
"""
お空の窓 (Weather Moon Stars) PyInstaller設定ファイル

このファイルでexe化の設定を管理します。
使用方法: pyinstaller weather_moon_stars.spec
"""

import os
from PyInstaller.utils.hooks import collect_data_files

# プロジェクトのルートパスを取得
ROOT_PATH = os.path.abspath('.')

# データファイルの収集
datas = [
    # 星座データファイル
    ('../data/astrology_data.json', 'data'),
    # 設定ファイル
    ('../config/app_config.ini', 'config'),
    # アイコンファイル（存在する場合）
    ('app_icon.ico', '.'),
]

# 隠しインポート（wxPythonとephemで必要なもの）
hiddenimports = [
    'wx',
    'wx._core',
    'wx._html',
    'ephem',
    'requests',
    'geopy',
    'geopy.geocoders',
    'certifi',
    'urllib3',
    'charset_normalizer',
]

a = Analysis(
    ['main.py'],
    pathex=[ROOT_PATH],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'tkinter',
        'test',
        'unittest',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='お空の窓',  # 実行ファイル名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # コンソールウィンドウを非表示
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',  # アイコンファイル
    version_file=None,  # バージョン情報ファイル（必要に応じて追加）
)

# 単一ファイル版（オプション）
# 以下のコメントを外すと、単一のexeファイルが生成されます
"""
exe_onefile = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='お空の窓_単一ファイル版',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
    onefile=True,  # 単一ファイルオプション
)
"""