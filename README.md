# games

个人小工具与小游戏合集。全部为单文件 HTML、零依赖、双击即玩，另含一个视频实时翻译工具。

## 项目清单

### 小游戏

| 项目 | 说明 | 玩法 |
|------|------|------|
| [ant-blocks.html](ant-blocks.html) | 蚂蚁搬方块 | 消除/搬运类小游戏 |
| [block-puzzle-ocean.html](block-puzzle-ocean.html) | 方块拼图·海洋历险 | 9×9 拖拽消除 + 像素画闯关，本地存档 |

### 家庭物品位置备忘工具

| 项目 | 说明 |
|------|------|
| [family-memory.html](family-memory.html) | 网页版：家庭物品（钥匙、充电宝等）位置录入与查找，本地存储 |
| [family-memory-app/](family-memory-app/) | Android App 工程：原生 WebView 壳，数据 localStorage 持久化 |
| [family-memory-site/](family-memory-site/) | 发布用静态副本（线上版入口） |

### 视频实时翻译

| 项目 | 说明 |
|------|------|
| [video-translator/](video-translator/) | Edge 视频实时翻译：后端抓取扬声器音频 + faster-whisper 识别 + WebSocket 推送，前端浏览器扩展叠加字幕 |

## 快速开始

- **小游戏 / 备忘工具网页版**：直接用浏览器打开对应 `.html` 文件即可，无需任何依赖。
- **家庭物品备忘 Android 版**：用 Android Studio 打开 `family-memory-app/`，Build → Generate APK。详见 [family-memory-app/README.md](family-memory-app/README.md)。
- **视频翻译器**：见 [video-translator/README.md](video-translator/README.md)。

## 技术栈

- 前端：纯 HTML + CSS + JavaScript，零框架、零构建
- Android：Java + WebView（WebViewAssetLoader）
- 翻译器：Python（faster-whisper）+ 浏览器扩展

## 目录结构

```
games/
├── ant-blocks.html              蚂蚁搬方块
├── block-puzzle-ocean.html      方块拼图·海洋历险
├── family-memory.html           家庭物品备忘（网页版）
├── family-memory-app/           家庭物品备忘（Android 工程）
├── family-memory-site/          家庭物品备忘（发布副本）
├── video-translator/            视频实时翻译
└── .gitignore
```

## 许可

个人项目，仅供学习与自用。
