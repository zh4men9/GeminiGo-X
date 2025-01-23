# 🎮 GeminiGo-X

<div align="center">

![GeminiGo-X Logo](assets/logo.png)

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyQt Version](https://img.shields.io/badge/PyQt-6.4.0%2B-orange.svg)](https://pypi.org/project/PyQt6/)
[![Gemini](https://img.shields.io/badge/Gemini-AI-purple.svg)](https://deepmind.google/technologies/gemini/)

*使用 Google Gemini 大语言模型的智能五子棋游戏* 🎯

[English](README_EN.md) | 简体中文

</div>

## ✨ 特性

- 🤖 集成 Google Gemini 大语言模型作为 AI 对手
- 🎨 现代化的用户界面，支持经典和现代两种主题
- 🎯 支持人机对战和双人对战模式
- 🔄 支持悔棋、重新开始等基本功能
- 🏆 智能判定胜负，实时显示游戏状态
- 🌐 支持残局模式和闯关模式（开发中）

## 🖼️ 预览

![游戏界面预览](assets/preview.png)

## 🚀 快速开始

### 前置要求

- Python 3.9 或更高版本
- Google Gemini API 密钥
- 能够访问 Google API 的网络环境

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/GeminiGo-X.git
cd GeminiGo-X
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

### 配置

1. 获取 Gemini API 密钥：
   - 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
   - 创建新的 API 密钥

2. 配置代理（如果需要）：
```python
# main.py
os.environ['http_proxy'] = 'http://your-proxy:port'
os.environ['https_proxy'] = 'http://your-proxy:port'
```

### 运行

```bash
python main.py
```

## 🎮 使用说明

1. **开始游戏**
   - 启动游戏后默认为双人对战模式
   - 点击"启用AI"按钮并输入 Gemini API 密钥来开启 AI 对战模式

2. **游戏规则**
   - 黑子先手
   - 在 AI 模式下，玩家执黑子，AI 执白子
   - 任意一方形成连续五子即获胜

3. **功能按钮**
   - 悔棋：撤销上一步（AI 模式下撤销两步）
   - 重新开始：清空棋盘重新开始
   - 切换主题：在经典和现代主题间切换
   - 残局模式：加载预设的残局进行练习
   - 闯关模式：按难度逐级挑战（开发中）

## 🛠️ 技术栈

- **UI 框架**: PyQt6
- **AI 模型**: Google Gemini
- **编程语言**: Python 3.9+
- **依赖管理**: pip

## 📝 待办事项

- [ ] 添加更多的残局场景
- [ ] 实现闯关模式
- [ ] 添加游戏音效
- [ ] 支持保存和加载对局
- [ ] 添加排行榜功能
- [ ] 优化 AI 响应速度

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交改动：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 📄 开源协议

本项目基于 MIT 协议开源 - 查看 [LICENSE](LICENSE) 文件了解更多细节

## 🙏 致谢

- [Google Gemini](https://deepmind.google/technologies/gemini/) - 提供强大的 AI 能力
- [PyQt](https://riverbankcomputing.com/software/pyqt/intro) - 优秀的 GUI 框架
- [五子棋规则](https://zh.wikipedia.org/wiki/五子棋) - 游戏规则参考

## 📧 联系方式

- 项目维护者: Your Name
- Email: your.email@example.com
- 项目链接: [https://github.com/yourusername/GeminiGo-X](https://github.com/yourusername/GeminiGo-X)

---

<div align="center">

如果这个项目对你有帮助，请给它一个 ⭐️ Star！

</div> 