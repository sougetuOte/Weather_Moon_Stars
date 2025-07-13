---
cache_control: {"type": "ephemeral"}
---
# Technical Context - お空の窓

## Architecture Overview
```
┌─────────────────────────────────────────────┐
│           wxPython GUI Application          │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────────┐ │
│  │   Weather   │  │   Astronomy Info     │ │
│  │   Display   │  │  - Moon Age         │ │
│  │   Panel     │  │  - Moon Sign        │ │
│  └─────────────┘  └──────────────────────┘ │
├─────────────────────────────────────────────┤
│              API Layer                      │
│  ┌─────────────┐  ┌──────────────────────┐ │
│  │ Open-Meteo  │  │   Astronomy Calc     │ │
│  │     API     │  │   (ephem library)    │ │
│  └─────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Technology Stack Details

### ⚠️ Windows PowerShell環境仕様（重要）
- **Python実行**: `"/c/micromamba/python.exe"` のパス指定必須（""で囲む）
- **パッケージ管理**: conda必須 - pipは使用不可
- **環境**: micromamba/conda環境での開発・実行
- **実行方法**: `conda run python script.py` 推奨

### Frontend
- **wxPython** v4.2.1
  - Cross-platform native GUI
  - TextCtrl for display
  - Button controls for actions
  - Clipboard integration

### Backend
- **Python** v3.12.5
  - Type hints対応
  - async/await対応（将来の拡張用）
  - conda環境で安定実行

### Libraries
- **requests** v2.25.1 - HTTP通信
- **ephem** v3.7.7.1 - 天体計算（月齢、黄道座標）
- **geopy** (予定) - ジオコーディング（都市名→緯度経度）
- **pyperclip** (wxPython内蔵) - クリップボード操作

## Development Environment (Windows PowerShell)
```bash
# ⚠️ Windows PowerShell環境での正しいセットアップ
# conda環境使用（pyenv不使用）
conda install python=3.12.5
conda install geopy=2.4.1 requests=2.25.1 ephem -c conda-forge

# パッケージ管理はconda必須（pipは使用しない）
# conda install package-name -c conda-forge

# Python実行時のパス指定
"/c/micromamba/python.exe" --version
```

## Startup Procedures
```bash
# 開発環境
cd src
python main.py

# 本番環境（exe化後）
./dist/お空の窓.exe
```

## API Design
### Open-Meteo API (新規実装)
- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Parameters**:
  - latitude, longitude: 地点座標
  - hourly: temperature_2m, precipitation_probability, weathercode
  - timezone: Asia/Tokyo
  - forecast_days: 1

### Geocoding API (Nominatim)
- **Purpose**: 都市名→緯度経度変換
- **Library**: geopy.geocoders.Nominatim

## Configuration Files
- **app_config.ini**: APIキー、最終検索都市名
- **astrology_data.json**: 星座定義データ
- **.python-version**: Python 3.12.5指定

## Performance Requirements
- 起動時間: 3秒以内
- API応答: 5秒以内でタイムアウト
- メモリ使用量: 100MB以下

## Security Considerations
- APIキーは設定ファイルで管理（gitignore対象）
- HTTPSのみ使用
- ユーザー入力のサニタイズ

## Known Constraints & Issues
- **OpenWeatherMap精度問題**: 気温、降水確率、現在天気すべて不正確
- **日本国内限定**: 海外都市は対象外
- **exe化**: PyInstallerでの配布準備が未着手