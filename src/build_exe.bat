@echo off
echo ========================================
echo お空の窓 exe化ビルドスクリプト
echo ========================================
echo.

REM Python環境の確認
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonが見つかりません
    echo Pythonをインストールしてください
    pause
    exit /b 1
)

echo Pythonバージョン:
python --version
echo.

REM PyInstallerの確認とインストール
echo PyInstallerを確認中...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstallerが見つかりません。インストールします...
    pip install pyinstaller
    if errorlevel 1 (
        echo エラー: PyInstallerのインストールに失敗しました
        pause
        exit /b 1
    )
) else (
    echo PyInstallerは既にインストールされています
)
echo.

REM ビルドの実行
echo ビルドを開始します...
python build_exe.py
if errorlevel 1 (
    echo.
    echo ====== 手動ビルドを試みます ======
    pyinstaller weather_moon_stars.spec
)

echo.
echo ビルド処理が完了しました
echo distフォルダを確認してください
pause