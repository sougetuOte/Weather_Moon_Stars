@echo off
echo ========================================
echo お空の窓 exe化ビルドスクリプト (conda版)
echo ========================================
echo.

REM conda環境でPyInstallerをインストール・実行
echo conda環境 'weather' でビルドを実行します...
echo.

REM PyInstallerのインストール確認
echo PyInstallerの確認とインストール...
conda run -n weather pip install pyinstaller
echo.

REM srcディレクトリに移動
cd /d %~dp0
echo 現在のディレクトリ: %CD%
echo.

REM ビルドの実行
echo ビルドを開始します...
conda run -n weather python build_exe.py
if errorlevel 1 (
    echo.
    echo ====== 手動ビルドを試みます ======
    conda run -n weather pyinstaller weather_moon_stars.spec
)

echo.
echo ビルド処理が完了しました
echo distフォルダを確認してください
pause