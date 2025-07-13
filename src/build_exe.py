#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
お空の窓 exe化ビルドスクリプト

このスクリプトを実行すると、PyInstallerを使用してexeファイルを生成します。
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime


def check_requirements():
    """必要な環境をチェック"""
    print("🔍 環境チェック中...")
    
    # PyInstallerの確認
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} が見つかりました")
    except ImportError:
        print("❌ PyInstallerがインストールされていません")
        print("実行: pip install pyinstaller")
        return False
    
    # 必要なファイルの確認
    required_files = [
        'main.py',
        'weather_moon_stars.spec',
        'app_icon.ico',
        '../data/astrology_data.json'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 必要なファイルが見つかりません: {file}")
            return False
    
    print("✅ すべての必要ファイルが見つかりました")
    return True


def clean_build():
    """ビルドディレクトリをクリーンアップ"""
    print("\n🧹 ビルドディレクトリをクリーンアップ中...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  削除: {dir_name}/")
    
    # .specファイルのバックアップ以外の.specファイルを削除
    for file in os.listdir('.'):
        if file.endswith('.spec') and file != 'weather_moon_stars.spec':
            os.remove(file)
            print(f"  削除: {file}")


def build_exe():
    """exeファイルをビルド"""
    print("\n🔨 exeファイルをビルド中...")
    
    # PyInstallerコマンドを実行
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'weather_moon_stars.spec'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ ビルド成功！")
            return True
        else:
            print("❌ ビルドに失敗しました")
            print("エラー出力:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ ビルド中にエラーが発生しました: {e}")
        return False


def create_distribution():
    """配布用パッケージを作成"""
    print("\n📦 配布用パッケージを作成中...")
    
    # 配布用ディレクトリ名（バージョンと日付を含む）
    version = "1.0"  # バージョン番号を適宜更新
    date_str = datetime.now().strftime("%Y%m%d")
    dist_name = f"WeatherMoonStars_v{version}_{date_str}"
    dist_path = os.path.join('dist', dist_name)
    
    # 配布用ディレクトリを作成
    os.makedirs(dist_path, exist_ok=True)
    
    # 必要なファイルをコピー
    files_to_copy = [
        ('dist/お空の窓.exe', 'お空の窓.exe'),
        ('README_new.md', 'README_ja.txt'),
        ('READMEen_new.md', 'README_en.txt'),
        ('QUICK_START_ja.md', 'QUICK_START_ja.txt'),
        ('QUICK_START_en.md', 'QUICK_START_en.txt'),
    ]
    
    for src, dst in files_to_copy:
        src_path = src
        dst_path = os.path.join(dist_path, dst)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"  コピー: {dst}")
        else:
            print(f"  ⚠️ ファイルが見つかりません: {src}")
    
    # dataディレクトリをコピー
    data_src = '../data'
    data_dst = os.path.join(dist_path, 'data')
    if os.path.exists(data_src):
        shutil.copytree(data_src, data_dst, dirs_exist_ok=True)
        print(f"  コピー: data/")
    
    # ZIPファイルを作成
    print(f"\n🗜️ ZIPファイルを作成中...")
    zip_name = f"{dist_name}.zip"
    shutil.make_archive(
        os.path.join('dist', dist_name),
        'zip',
        'dist',
        dist_name
    )
    print(f"✅ 配布用パッケージを作成しました: dist/{zip_name}")
    
    return dist_path, zip_name


def main():
    """メイン処理"""
    print("🌤️ お空の窓 ビルドスクリプト")
    print("=" * 50)
    
    # 環境チェック
    if not check_requirements():
        print("\n❌ ビルドを中止しました")
        return 1
    
    # クリーンアップ
    clean_build()
    
    # ビルド実行
    if not build_exe():
        print("\n❌ ビルドに失敗しました")
        return 1
    
    # 配布用パッケージ作成
    dist_path, zip_name = create_distribution()
    
    print("\n✅ すべての処理が完了しました！")
    print(f"\n配布用ファイル:")
    print(f"  - フォルダ: {dist_path}")
    print(f"  - ZIP: dist/{zip_name}")
    print(f"\nテスト実行: {os.path.join(dist_path, 'お空の窓.exe')}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())