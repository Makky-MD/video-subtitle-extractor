# -*- coding: utf-8 -*-
"""
AI字幕工具箱 - 主程序入口
环境校验 + 异常捕获 + 中文友好提示
"""

import os
import sys
from pathlib import Path

# ===== 把当前项目根目录加入模块搜索路径，解决找不到batch_trans问题 =====
BASE_DIR = Path(__file__).parent.resolve()
sys.path.append(str(BASE_DIR))

BIN_DIR = BASE_DIR / "bin"
CACHE_DIR = BASE_DIR / "cache"


def pause_exit(code=0):
    """暂停等待用户按回车，防止闪退"""
    try:
        input("\n按回车键退出...")
    except EOFError:
        pass
    sys.exit(code)


def check_environment():
    """环境完整性检查"""
    errors = []
    
    # 检查ffmpeg
    ffmpeg_path = BIN_DIR / "ffmpeg.exe"
    if not ffmpeg_path.exists():
        errors.append("缺少 bin\\ffmpeg.exe 文件")
    
    # 检查ffprobe
    ffprobe_path = BIN_DIR / "ffprobe.exe"
    if not ffprobe_path.exists():
        errors.append("缺少 bin\\ffprobe.exe 文件")
    
    # 检查配置文件
    config_path = BASE_DIR / "config.ini"
    if not config_path.exists():
        errors.append("缺少 config.ini 配置文件")
    
    # 检查模型缓存目录
    whisper_cache = CACHE_DIR / "whisper"
    if not whisper_cache.exists() or not any(whisper_cache.iterdir()):
        errors.append("cache\\whisper 目录为空，缺少模型文件")
    
    if errors:
        print("=" * 50)
        print("【环境检测失败】缺少以下必要文件：")
        for e in errors:
            print(f"  ✗ {e}")
        print("\n请确认解压完整，不要删除或移动任何文件")
        print("如仍有问题，请重新解压压缩包")
        print("=" * 50)
        return False
    
    print("✓ 环境检测通过")
    return True


def print_banner():
    print("=" * 50)
    print("       AI 字幕工具箱  -  Whisper 批量转写")
    print("=" * 50)
    print()


def main():
    print_banner()
    
    # 环境检测
    print("正在检测运行环境...")
    if not check_environment():
        pause_exit(1)
    
    # 导入并运行批量转写
    try:
        import batch_trans
        batch_trans.run_batch()
    except ImportError as e:
        print(f"\n【错误】缺少必要的依赖库：{e}")
        print("请确认 python-embed 目录完整，依赖已正确安装")
        pause_exit(1)
    except Exception as e:
        print(f"\n【运行错误】{type(e).__name__}: {e}")
        print("\n常见问题：")
        print("  1. 视频文件损坏或格式不支持")
        print("  2. 显存不足，请改用更小的模型或cpu模式")
        print("  3. 模型文件不完整，请检查cache目录")
        pause_exit(1)
    
    pause_exit(0)


if __name__ == "__main__":
    main()