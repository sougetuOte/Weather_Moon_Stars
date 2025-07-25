# 🌤️ お空の窓 (Weather Moon Stars)

> **正確な天気予報と美しい天体情報を、ひとつの窓から**

## 💡 概要

高精度な天気予報と、月齢・星座情報を美しく統合したデスクトップアプリケーション。  
Open-Meteo APIの採用により、**東京都千代田区**や**大阪市北区**のような詳細な住所でも正確な天気予報を実現しました。

### ✨ 主な機能

- 🌡️ **高精度天気予報**: 24時間先までの気温、湿度、風速、降水確率
- 🌙 **天体情報**: リアルタイム月齢計算と月の星座表示
- 📋 **便利機能**: ワンクリックでクリップボードにコピー
- 🔍 **詳細住所対応**: 東京23区レベルの詳細な地名に対応

## 🚀 使い方

### exe版（配布版）の場合

1. **起動**: `お空の窓.exe`をダブルクリック
2. **都市名入力**: テキストボックスに都市名を入力（例：東京都渋谷区、大阪市北区）
3. **検索実行**: 「実行」ボタンをクリックまたはEnterキー
4. **結果確認**: 天気予報と月齢・星座情報が表示されます
5. **コピー**: 「コピー」ボタンで結果をクリップボードへ

**注意**: APIキーの設定は不要です。インターネット接続が必要です。

### 開発版（ソースコード）の場合

詳細は`install_dev.txt`を参照してください。

## 📊 機能詳細

### 天気予報
- 現在の天気状況
- 3時間ごとの24時間予報
- 気温、降水確率、風速、湿度の表示

### 天体情報
- 月齢（小数点第2位まで）
- 月が位置する星座
- 星座の説明文

## 🔧 技術仕様

- **天気データ**: Open-Meteo API（無料、APIキー不要）
- **天体計算**: ephemライブラリによる高精度計算
- **GUI**: wxPythonによるクロスプラットフォーム対応
- **言語**: Python 3.12

## 📝 ライセンス

Copyright (c) 2023-2025 sougetuOte  
Released under the MIT license  
https://opensource.org/licenses/mit-license.php

## 📞 連絡先

- **GitHub**: https://github.com/sougetuOte/Weather_Moon_Stars
- **Email**: magician@amateur-magician.life

## 🙏 謝辞

- Open-Meteo: 高精度な天気データの提供
- ephem: 正確な天体計算ライブラリ
- wxPython: 美しいGUIフレームワーク

---
*最終更新: 2025年1月*