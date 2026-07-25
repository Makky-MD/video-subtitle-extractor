# -*- coding: utf-8 -*-
"""
批量视频转写核心模块
基于 OpenAI Whisper (MIT License)
"""

import os
import sys
import configparser
from pathlib import Path

# ===== 强制设置模型缓存目录，优先读取本地模型 =====
BASE_DIR = Path(__file__).parent.resolve()
CACHE_DIR = BASE_DIR / "cache"
os.environ["WHISPER_CACHE_DIR"] = str(CACHE_DIR)
os.environ["HF_HUB_OFFLINE"] = "1"  # 禁止在线下载

# ===== ffmpeg 路径加入环境变量，供whisper调用 =====
BIN_DIR = BASE_DIR / "bin"
os.environ["PATH"] = str(BIN_DIR) + os.pathsep + os.environ.get("PATH", "")

# ===== 读取配置 =====
def load_config():
    config = configparser.ConfigParser()
    config_path = BASE_DIR / "config.ini"
    if not config_path.exists():
        raise FileNotFoundError("配置文件 config.ini 不存在，请检查文件完整性")
    config.read(config_path, encoding="utf-8")
    return config

# ===== 扫描视频文件 =====
def scan_videos():
    video_exts = [".mp4", ".mov", ".mkv", ".avi", ".flv"]
    videos = []
    for ext in video_exts:
        videos.extend(list(BASE_DIR.glob(f"*{ext}")))
    # 去重并排序
    videos = sorted(set(videos))
    return videos

# ===== 格式化时间戳为SRT格式 =====
def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

# ===== 生成SRT字幕文件 =====
def save_srt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

# ===== 生成TXT文稿 =====
def save_txt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(seg["text"].strip() + "\n")

# ===== 单个视频转写 =====
def transcribe_video(video_path, model, language):
    print(f"\n正在转写：{video_path.name}")
    print("-" * 50)
    
    result = model.transcribe(
        str(video_path),
        language=language if language != "auto" else None,
        verbose=False,
        initial_prompt="使用简体中文，带标点符号，正常断句",
        word_timestamps=False
    )
    
    segments = result["segments"]
    base_name = video_path.stem
    
    # 保存SRT
    srt_path = video_path.parent / f"{base_name}.srt"
    save_srt(segments, srt_path)
    print(f"  ✓ 已生成字幕：{base_name}.srt")
    
    # 保存TXT
    txt_path = video_path.parent / f"{base_name}.txt"
    save_txt(segments, txt_path)
    print(f"  ✓ 已生成文稿：{base_name}.txt")
    
    return len(segments)

# ===== 主批量处理函数 =====
def run_batch():
    config = load_config()
    
    model_size = config.get("Whisper", "model_size", fallback="small")
    language = config.get("Whisper", "language", fallback="zh")
    device = config.get("Whisper", "device", fallback="cpu")
    
    # 扫描视频
    videos = scan_videos()
    if not videos:
        print("\n【提示】当前目录下没有找到视频文件")
        print("请把 mp4 / mov / mkv / avi / flv 格式的视频放到工具根目录，再重新启动")
        return
    
    print(f"\n找到 {len(videos)} 个视频文件：")
    for v in videos:
        print(f"  - {v.name}")
    
    # 加载模型
    print(f"\n正在加载 Whisper 模型 [{model_size}] ...")
    print("（首次加载较慢，请耐心等待）")
    
    try:
        import whisper
        model = whisper.load_model(model_size, device=device, download_root=str(CACHE_DIR))
    except Exception as e:
        print(f"\n【错误】模型加载失败：{e}")
        print("请检查 cache/whisper 目录下是否有对应模型文件")
        return
    
    print("模型加载完成，开始转写...\n")
    
    # 批量转写
    success = 0
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] ", end="")
        try:
            count = transcribe_video(video, model, language)
            success += 1
            print(f"  完成，共 {count} 条字幕")
        except Exception as e:
            print(f"\n  ✗ 转写失败：{e}")
    
    # 总结
    print("\n" + "=" * 50)
    print(f"批量转写完成！成功 {success} 个，失败 {len(videos) - success} 个")
    print("字幕文件和文稿已保存在视频同目录下")


if __name__ == "__main__":
    run_batch()