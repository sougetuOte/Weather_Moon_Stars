@echo off
echo お空の窓 - シンプルビルド
echo.

REM srcディレクトリに移動
cd /d %~dp0

REM condaでPyInstallerを実行
echo PyInstallerでビルドを開始...
conda run -n weather pyinstaller weather_moon_stars.spec --clean --noconfirm

echo.
echo ビルド完了
echo distフォルダを確認してください
pause