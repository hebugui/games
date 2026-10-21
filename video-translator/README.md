# 视频实时翻译 (英/日译中)

抓取系统扬声器音频 → 本地语音识别 → 翻译 → 在网页上叠加实时中文字幕。

## 结构
```
backend/     Python 转写后台 (抓音频 + faster-whisper + WebSocket 推送)
extension/   Edge 插件 (接收字幕并叠加显示)
```

## 使用步骤

### 1. 启用"立体声混音"
Windows：右键任务栏音量 → 声音设置 → 输入设备 → 管理声音设备 → 启用「立体声混音(Stereo Mix)」。没有该选项说明声卡驱动不支持，需装驱动或用虚拟声卡(如 VB-Cable)。

### 2. 跑转写后台
```bash
cd backend
pip install -r requirements.txt
python transcriber.py --list-devices      # 查看输入设备编号
python transcriber.py --device <编号>      # 默认自动检测语言、small 模型
# 指定语言:
python transcriber.py --source-lang ja --device <编号>   # 日译中
python transcriber.py --source-lang en --device <编号>   # 英译中
```

首次运行会下载 whisper 模型(默认 small)。

### 3. 加载 Edge 插件
1. Edge 地址栏输入 `edge://extensions`
2. 打开「开发人员模式」
3. 「加载解压缩的扩展」→ 选择 `extension/` 目录

打开任意视频页面，扬声器一有声音，页面底部就会出现原文+中文译文字幕。

## 说明

- **翻译引擎**：`Translator` 类当前是占位(返回原文)。接真实翻译 API 时改 `transcriber.py` 里的 `Translator.translate()`，可接百度/腾讯/DeepL 等。
- **识别引擎可切换**：`--engine local`(本地免费, 默认) / `--engine cloud`(预留, 需在 `CloudTranscriber` 里接云 API)。
- **手机端**：暂未实现，后续可加(手机浏览器访问电脑开的本地页面同步显示字幕)。
