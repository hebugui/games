# -*- coding: utf-8 -*-
"""
视频实时翻译 - 转写核心
抓取系统扬声器音频(立体声混音) -> faster-whisper 识别 -> 翻译 -> 推送给 WebSocket 字幕服务

引擎可切换：
  - 本地: faster-whisper (默认, 免费离线)
  - 云端: 预留接口, 后续接 OpenAI Whisper API / Google Speech 等

用法:
  python transcriber.py --source-lang ja --target-lang zh --device 1
"""
import argparse
import threading
import time
import queue

import numpy as np
import sounddevice as sd


class AudioCapture:
    """抓取系统扬声器音频。Windows 需启用"立体声混音(Stereo Mix)"作为输入设备。"""

    def __init__(self, sample_rate=16000, device=None, chunk_ms=500):
        self.sample_rate = sample_rate
        self.device = device
        self.chunk = int(sample_rate * chunk_ms / 1000)
        self.q = queue.Queue(maxsize=100)
        self._stop = threading.Event()

    def _callback(self, indata, frames, time_info, status):
        # 取单声道均值，丢进队列
        mono = indata.mean(axis=1) if indata.ndim > 1 else indata
        self.q.put(mono.copy())

    def start(self):
        sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            device=self.device,
            callback=self._callback,
            blocksize=self.chunk,
        ).start()

    def stop(self):
        self._stop.set()


class LocalWhisperTranscriber:
    """本地 faster-whisper 转写。"""

    def __init__(self, model_size="small", source_lang=None):
        from faster_whisper import WhisperModel
        self.source_lang = source_lang  # None 表示自动检测
        self.model = WhisperModel(model_size, device="auto", compute_type="int8")

    def transcribe(self, audio: np.ndarray, sample_rate=16000):
        audio = audio.astype(np.float32) / 32768.0 if audio.dtype != np.float32 else audio
        segments, info = self.model.transcribe(
            audio,
            language=self.source_lang,
            beam_size=5,
            vad_filter=True,
        )
        text = "".join(s.text for s in segments)
        detected = info.language
        return text.strip(), detected


class CloudTranscriber:
    """云端语音识别预留接口。后续在此实现 OpenAI Whisper API 等。"""

    def __init__(self, api_key=None, provider=None):
        self.api_key = api_key
        self.provider = provider or "openai"

    def transcribe(self, audio: np.ndarray, sample_rate=16000):
        # TODO: 接云端 API。当前占位, 抛异常提示未实现。
        raise NotImplementedError(
            "云端识别尚未实现。请使用 --engine local, 或在此类中接入你的云 API。"
        )


class Translator:
    """翻译器。默认用免费本地占位, 可替换为任意翻译 API。"""

    def __init__(self, target_lang="zh"):
        self.target_lang = target_lang

    def translate(self, text: str):
        # 占位: 不翻译直接返回原文。接入真实翻译 API 时替换此处。
        # 例如调用 requests.post 到你的翻译服务。
        return text


def build_transcriber(engine, model_size, source_lang):
    if engine == "local":
        return LocalWhisperTranscriber(model_size=model_size, source_lang=source_lang)
    return CloudTranscriber()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-lang", default=None, help="源语言代码, 如 en/ja; None 自动检测")
    ap.add_argument("--target-lang", default="zh", help="目标语言")
    ap.add_argument("--engine", default="local", choices=["local", "cloud"], help="识别引擎")
    ap.add_argument("--model", default="small", help="whisper 模型大小: tiny/base/small/medium/large")
    ap.add_argument("--device", type=int, default=None, help="音频输入设备编号(立体声混音)")
    ap.add_argument("--list-devices", action="store_true", help="列出所有音频输入设备后退出")
    args = ap.parse_args()

    if args.list_devices:
        print(sd.query_devices())
        return

    transcriber = build_transcriber(args.engine, args.model, args.source_lang)
    print(f"[transcriber] 引擎={args.engine} 模型={args.model} 源语言={args.source_lang or 'auto'} -> 目标={args.target_lang}")

    # 通过 WebSocket 服务推送字幕(服务端在 server.py)
    from server import SubtitleServer
    server = SubtitleServer()
    threading.Thread(target=server.run, kwargs={"host": "127.0.0.1", "port": 8765}, daemon=True).start()
    time.sleep(0.5)

    capture = AudioCapture(device=args.device)
    capture.start()
    print("[capture] 开始抓取扬声器音频... (如无声音请启用'立体声混音'输入设备)")

    buf = []
    try:
        while True:
            try:
                chunk = capture.q.get(timeout=1.0)
            except queue.Empty:
                continue
            buf.append(chunk)
            # 每 3 秒聚合识别一次
            if sum(len(c) for c in buf) >= capture.sample_rate * 3:
                audio = np.concatenate(buf)
                buf.clear()
                text, detected = transcriber.transcribe(audio)
                if text:
                    translated = Translator(args.target_lang).translate(text)
                    print(f"[{detected}->{args.target_lang}] {text}")
                    print(f"    => {translated}")
                    server.broadcast({"src": text, "dst": translated, "lang": detected})
    except KeyboardInterrupt:
        capture.stop()
        print("[capture] 已停止")


if __name__ == "__main__":
    main()
