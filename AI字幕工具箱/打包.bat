@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 正在打包主程序...
echo.

pyinstaller --onefile --name "AI字幕工具箱" ^
    --paths "." ^
    --hidden-import whisper ^
    --hidden-import torch ^
    --hidden-import tiktoken ^
    --hidden-import numba ^
    --hidden-import batch_trans ^
    --add-data "batch_trans.py;." ^
    --collect-all whisper ^
    main.py

echo.
echo 打包完成！exe文件在 dist 目录下
pause