# 🎮 GeminiGo-X

<div align="center">

![GeminiGo-X Logo](assets/logo.png)

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyQt Version](https://img.shields.io/badge/PyQt-6.4.0%2B-orange.svg)](https://pypi.org/project/PyQt6/)
[![Gemini](https://img.shields.io/badge/Gemini-AI-purple.svg)](https://deepmind.google/technologies/gemini/)

*An Intelligent Gomoku (Five in a Row) Game Powered by Google Gemini LLM* 🎯

English | [简体中文](README.md)

</div>

## ✨ Features

- 🤖 Integrated with Google Gemini LLM as AI opponent
- 🎨 Modern UI with classic and modern themes
- 🎯 Support both AI vs Human and Human vs Human modes
- 🔄 Basic features like undo, restart
- 🏆 Smart win detection and real-time game status
- 🌐 Puzzle mode and campaign mode (under development)

## 🖼️ Preview

![Game Interface Preview](assets/preview.png)

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key
- Network access to Google API

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GeminiGo-X.git
cd GeminiGo-X
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

1. Get Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

2. Configure proxy (if needed):
```python
# main.py
os.environ['http_proxy'] = 'http://your-proxy:port'
os.environ['https_proxy'] = 'http://your-proxy:port'
```

### Run

```bash
python main.py
```

## 🎮 How to Play

1. **Start Game**
   - Default mode is Human vs Human
   - Click "Enable AI" button and enter Gemini API key to enable AI mode

2. **Game Rules**
   - Black moves first
   - In AI mode, player plays black, AI plays white
   - Win by forming five in a row

3. **Function Buttons**
   - Undo: Take back last move (two moves in AI mode)
   - Restart: Clear board and start new game
   - Toggle Theme: Switch between classic and modern themes
   - Puzzle Mode: Practice with preset scenarios
   - Campaign Mode: Challenge levels with increasing difficulty (coming soon)

## 🛠️ Tech Stack

- **UI Framework**: PyQt6
- **AI Model**: Google Gemini
- **Programming Language**: Python 3.9+
- **Dependency Management**: pip

## 📝 TODO

- [ ] Add more puzzle scenarios
- [ ] Implement campaign mode
- [ ] Add sound effects
- [ ] Support save/load game
- [ ] Add leaderboard
- [ ] Optimize AI response time

## 🤝 Contributing

Contributions are welcome! Feel free to submit Issues and Pull Requests.

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add some AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) - For powerful AI capabilities
- [PyQt](https://riverbankcomputing.com/software/pyqt/intro) - For excellent GUI framework
- [Gomoku Rules](https://en.wikipedia.org/wiki/Gomoku) - For game rules reference

## 📧 Contact

- Project Maintainer: Your Name
- Email: your.email@example.com
- Project Link: [https://github.com/yourusername/GeminiGo-X](https://github.com/yourusername/GeminiGo-X)

---

<div align="center">

If this project helps you, please give it a ⭐️ Star!

</div> 