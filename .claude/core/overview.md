---
cache_control: {"type": "ephemeral"}
---
# Project Overview - お空の窓 (Weather Moon Stars)
tags: #overview #project #summary

## ⚠️ 重要：Windows PowerShell環境制約（必須）
- **パス指定**: `"/c/micromamba/python.exe" --version` のように""で囲む必須
- **パッケージ管理**: pipではなく**conda必須** - `conda install package-name`
- **環境**: Windows PowerShellでのconda環境使用が確定仕様
- **実行例**: `conda run python script.py` または `"/c/micromamba/python.exe" script.py`

## 3-Line Summary
- **Purpose**: 高精度な天気予報と月齢・星座情報を提供するデスクトップアプリ #purpose #problem
- **Target**: 日本国内の個人ユーザー（天気・天体情報を日常的に確認したい人） #target #users
- **Success Criteria**: OpenWeatherMapより正確な天気予報の実現 #success #metrics

## Project Basic Information
- **Start Date**: 2024年（既存プロジェクト）
- **Refactoring Date**: 2025年1月13日
- **Current Progress**: 基本機能実装済み、API精度改善中（70%）

## Core Features (Priority Order)
1. **天気予報表示**: Open-Meteo APIによる24時間先までの高精度予報 #feature #core #p1
2. **月齢計算**: ephemライブラリによる正確な月齢表示 #feature #core #p2
3. **月の星座**: 現在の月がどの星座にあるかを表示 #feature #core #p3
4. **クリップボード連携**: 情報をワンクリックでコピー #feature #core #p4

## Technology Stack
- **Language**: Python 3.12.5 #tech #language
- **Framework**: wxPython 4.2.1 (GUI) #tech #framework
- **DB**: なし（設定ファイルのみ） #tech #database
- **Others**: ephem, requests, geopy（予定） #tech #tools

## Constraints & Assumptions
- 日本国内のみ対応
- デスクトップアプリケーション（Windows/Mac/Linux）
- 個人利用（1日1回程度のAPI使用）

## Success Criteria & Progress
- [x] 基本的なGUIと機能の実装 - 完了
- [ ] OpenWeatherMapからOpen-Meteoへの移行 - 実装中
- [ ] 天気予報精度の大幅改善 - 検証待ち
- [ ] exe化による配布準備 - 未着手

## Problem Definition
OpenWeatherMap APIの精度が低く（気温、降水確率、現在天気すべて不正確）、実用的な天気予報アプリとして機能していない。

## User Value
正確な天気予報と天体情報を、美しいGUIで簡単に確認できる。

Detailed technical information → @.claude/context/tech.md
Detailed specifications → @docs/requirements.md