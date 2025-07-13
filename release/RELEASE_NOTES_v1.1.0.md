# GitHub Release Notes for v1.1.0

## Release Title
```
v1.1.0: お空の窓 - 完全exe化配布版
```

## Release Notes
```markdown
# 🎉 v1.1.0 - お空の窓 完全exe化配布版リリース

## 🌟 主な新機能

### 🚀 exe化対応
- **Python環境不要**: 単体実行可能なexeファイル（26.1MB）
- **簡単インストール**: ダウンロードして即座に使用可能

### 🌤️ 高精度天気予報
- **Open-Meteo API採用**: OpenWeatherMapより大幅に精度向上
- **APIキー不要**: 無料で永続利用可能
- **詳細住所対応**: 東京23区レベルの精密な地名に対応

### 🛡️ 堅牢性向上
- **3段階フォールバック**: 設定エラーでも動作継続
- **エラーハンドリング強化**: ユーザーフレンドリーなエラーメッセージ
- **安定動作**: 予期しない問題でもアプリケーション停止なし

## 📦 配布内容

- `お空の窓.exe` - メインアプリケーション
- `README_ja.md` - 日本語使用説明書
- `README_en.md` - English documentation
- `QUICK_START_ja.md` - 日本語クイックスタート
- `QUICK_START_en.md` - English quick start
- `CHANGELOG.md` - 詳細な変更履歴

## 🔄 v1.0.0からの主な改善

| 項目 | v1.0.0 | v1.1.0 |
|------|--------|--------|
| 実行環境 | Python環境必須 | exe単体実行可能 |
| API | OpenWeatherMap | Open-Meteo (高精度) |
| APIキー | 必須 | 不要 |
| 住所精度 | 都市レベル | 23区レベル |
| エラー対応 | 基本的 | 3段階フォールバック |

## 🚀 使い方

1. `Weather_Moon_Stars_v1.1.0.zip`をダウンロード
2. zipファイルを展開
3. `お空の窓.exe`をダブルクリックで起動
4. 都市名を入力して「実行」ボタンをクリック

詳細は同梱のREADMEファイルをご確認ください。

---

🤖 This release was prepared with Claude Code assistance.
```

## Manual Release Creation Instructions

1. **GitHubのリポジトリページに移動**
   - https://github.com/sougetuOte/Weather_Moon_Stars

2. **リリースページに移動**
   - "Releases" セクションをクリック
   - "Create a new release" をクリック

3. **リリース情報入力**
   - Tag: `v1.1.0` (既に作成済み)
   - Title: `v1.1.0: お空の窓 - 完全exe化配布版`
   - Description: 上記のRelease Notesをコピー&ペースト

4. **ファイル添付**
   - `release/Weather_Moon_Stars_v1.1.0.zip` をアップロード

5. **リリース公開**
   - "Publish release" をクリック