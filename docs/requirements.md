---
cache_control: {"type": "ephemeral"}
---
# お空の窓 Requirements Specification

## 1. Project Overview

### 1.1 Purpose
高精度な天気予報と天体情報（月齢・星座）を提供し、日常生活に役立つデスクトップアプリケーション

### 1.2 Scope
- Users: 日本国内の個人ユーザー
- Environment: Windows/Mac/Linux デスクトップ環境
- Constraints: 日本国内限定、個人利用想定（1日1回程度）

### 1.3 Technology Stack
- **Frontend**: wxPython 4.2.1
- **Backend**: Python 3.12.5
- **Database**: なし（設定ファイルのみ）
- **Others**: ephem, requests, geopy（予定）

## 2. Functional Requirements

### 2.1 天気予報機能
#### 2.1.1 天気データ取得
- Open-Meteo APIから24時間分の天気データを取得
- 都市名入力→緯度経度変換→API呼び出し
- 取得項目：気温、降水確率、天気コード、風速、湿度

#### 2.1.2 天気情報表示
- 現在の天気と気温
- 1時間ごとの予報（24時間分）
- 日本語での天気説明（晴れ、曇り、雨など）

### 2.2 天体情報機能
#### 2.2.1 月齢計算
- ephemライブラリによる正確な月齢計算
- 小数点第2位まで表示

#### 2.2.2 月の星座表示
- 月の黄道座標から現在位置の星座を判定
- 12星座の日本語名と説明文を表示

### 2.3 ユーティリティ機能
#### 2.3.1 都市名保存
- 最後に検索した都市名を保存
- 次回起動時に自動入力

#### 2.3.2 クリップボード連携
- 表示内容をワンクリックでコピー
- コピー完了の通知表示

## 3. Non-Functional Requirements

### 3.1 Performance Requirements
- 起動時間：3秒以内
- API応答：5秒以内（タイムアウト設定）
- メモリ使用量：100MB以下

### 3.2 Usability Requirements
- シンプルで直感的なUI
- 日本語表示
- エラー時の分かりやすいメッセージ

### 3.3 Security Requirements
- HTTPS通信のみ使用
- APIキーの安全な管理（設定ファイル）
- ユーザー入力のサニタイズ

### 3.4 Development and Operation Requirements
- Version control: Git
- Development environment: Python 3.12.5 + pyenv
- Testing: 手動テスト中心
- Deployment: PyInstallerによるexe化（予定）

## 4. API Design

### 4.1 Open-Meteo API
```
GET https://api.open-meteo.com/v1/forecast
Parameters:
- latitude: 緯度
- longitude: 経度
- hourly: temperature_2m,precipitation_probability,weathercode,windspeed_10m,relativehumidity_2m
- timezone: Asia/Tokyo
- forecast_days: 1
```

### 4.2 Geocoding (Nominatim)
```python
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="okora-no-mado")
location = geolocator.geocode("東京都")
```

## 5. Directory Structure

```
Weather_Moon_Stars/
├── .claude/           # Memory Bank
├── src/               # ソースコード
│   ├── api/          # API関連
│   ├── features/     # 機能モジュール
│   ├── gui/          # GUI関連
│   ├── utils/        # ユーティリティ
│   └── main.py       # エントリーポイント
├── data/              # データファイル
├── config/            # 設定ファイル
├── docs/              # ドキュメント
├── CLAUDE.md          # プロジェクト設定
├── .clauderules       # プロジェクト固有の学習
├── requirements.txt   # 依存関係
└── README.md          # プロジェクト説明
```

## 6. Development Schedule

### Phase 1: Open-Meteo API実装（現在）
- API仕様調査
- 実装設計
- コード実装とテスト

### Phase 2: リファクタリング（今週）
- コード構造の整理
- エラーハンドリング強化
- パフォーマンス最適化

### Phase 3: 配布準備（来週）
- PyInstallerでのexe化
- インストーラー作成
- ドキュメント整備

## 7. Success Criteria

- [x] 基本的なGUIと機能の実装
- [ ] OpenWeatherMapより正確な天気予報の実現
- [ ] 安定したアプリケーション動作
- [ ] 簡単な配布とインストール

## 8. Risks and Countermeasures

| Risk | Impact | Probability | Countermeasure |
|------|--------|-------------|----------------|
| Open-Meteo APIの精度不足 | High | Low | 複数APIの併用を検討 |
| exe化での不具合 | Medium | Medium | 十分なテストとドキュメント作成 |
| 地名変換の精度 | Low | Medium | ユーザーによる緯度経度直接入力オプション |

## 9. Notes

- 将来的には複数のAPIを組み合わせてさらなる精度向上を検討
- UI/UXの改善は基本機能安定後に実施予定