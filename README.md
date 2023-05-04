# お空の窓
日本の天気予報と月星座、その解説を表示するプログラム

# 入手方法
https://github.com/sougetuOte/Weather_Moon_Stars
からgit cloneするか、zipファイルをダウンロードしてください。
https://www.amateur-magician.life/
からもzipファイルをダウンロード可能です。
ネットに詳しくない人はこちらかの方が楽かも知れません。

# ライセンス
Copyright (c) 2023 sougetuOte
Released under the MIT license
https://opensource.org/licenses/mit-license.php

# 用途
天気予報と月星座、その解説を得るためのプログラムです。日記を書く際に一々調べてコピペするのが面倒で作りました。
日本語またはアルファベットで都市名を入力しボタンを押すと、天気予報と月星座、その解説がテキストエリアとクリップボードに出力されます。
ただそれだけのプログラムです。

# 注意
OpenWeather( https://openweathermap.org/ )のAPIを使っていますので、使用者はAPIKEYを手に入れて登録する必要があります。
正直精度は低いです。本当は気象庁のデータが使えると良かったのですが、くじけました。情報募集。

# 使用方法
インストール方法は、install.txtに記載
プログラムを起動したら都市名を入れ、欲しいデータの日付を指定してください。最後にボタンを押したらテキストエリアとクリップボードにデータが貼り付けられます。

# ファイル構成
main.py: アプリケーションのエントリーポイント。GUIの初期化と実行を行います。
weather_gui.py: wxPythonを使用したGUIの定義を行います。
weather_api.py: 気象庁のXMLデータを取得し、パースして天気情報を取得します。
moon_age.py: 月齢計算のロジックを提供します。
astrology.py: 占星術の月星座と解説を提供します。外部テキストファイルを読み込みます。
clipboard.py: クリップボードへのテキストコピーを行うユーティリティを提供します。
config.py: アプリケーションの設定情報を提供します。外部テキストファイルのパスなどが含まれます。
astrology_data.json:占星術の星座についてのデータが格納されています。
app_config.ini:OpenWeatherのAPIキーと占星術データのファイル名を記載します。
README.md:このファイルです。
install.txtインストール方法が記載されています。

# 連絡先
Twitter：https://twitter.com/ETM08214742
e-mail：magician@amateur-magician.life
