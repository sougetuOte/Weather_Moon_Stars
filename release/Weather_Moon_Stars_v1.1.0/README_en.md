# 🌤️ Window to the Sky (Weather Moon Stars)

> **Accurate weather forecasts and beautiful celestial information from one window**

## 💡 Overview

A desktop application that beautifully integrates high-precision weather forecasts with moon phase and zodiac information.  
With the adoption of Open-Meteo API, we have achieved accurate weather forecasts even for detailed addresses like **Chiyoda-ku, Tokyo** or **Kita-ku, Osaka**.

### ✨ Key Features

- 🌡️ **High-Precision Weather**: Temperature, humidity, wind speed, and precipitation for the next 24 hours
- 🌙 **Celestial Information**: Real-time moon age calculation and current moon zodiac position
- 📋 **Convenient Features**: One-click copy to clipboard
- 🔍 **Detailed Address Support**: Supports district-level precision for major Japanese cities

## 🚀 How to Use

### For exe Version (Distribution)

1. **Launch**: Double-click `お空の窓.exe`
2. **Enter City**: Type city name in the text box (e.g., Shibuya-ku Tokyo, Kita-ku Osaka)
3. **Search**: Click "実行" button or press Enter
4. **View Results**: Weather forecast and moon/zodiac information will be displayed
5. **Copy**: Click "コピー" button to copy results to clipboard

**Note**: No API key required. Internet connection is necessary.

### For Development Version (Source Code)

Please refer to `install_dev_en.txt` for details.

## 📊 Feature Details

### Weather Forecast
- Current weather conditions
- 24-hour forecast in 3-hour intervals
- Temperature, precipitation probability, wind speed, and humidity

### Celestial Information
- Moon age (to 2 decimal places)
- Current moon zodiac position
- Zodiac description

## 🔧 Technical Specifications

- **Weather Data**: Open-Meteo API (Free, no API key required)
- **Celestial Calculations**: High-precision calculations using ephem library
- **GUI**: Cross-platform support with wxPython
- **Language**: Python 3.12

## 📝 License

Copyright (c) 2023-2025 sougetuOte  
Released under the MIT license  
https://opensource.org/licenses/mit-license.php

## 📞 Contact

- **GitHub**: https://github.com/sougetuOte/Weather_Moon_Stars
- **Email**: magician@amateur-magician.life

## 🙏 Acknowledgments

- Open-Meteo: For providing high-precision weather data
- ephem: For accurate celestial calculation library
- wxPython: For the beautiful GUI framework

---
*Last updated: January 2025*