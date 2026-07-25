@echo off
chcp 65001 >nul
title 安装依赖 - AI字幕工具箱

cd /d "%~dp0"

echo ========================================
echo   AI字幕工具箱 - 依赖安装
echo ========================================
echo.
echo 正在安装 Python 依赖包...
echo 使用清华镜像源加速，请耐心等待
echo.

"python-embed\python.exe" -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location

echo.
echo 安装 torch（Whisper核心依赖，体积较大，请耐心等待）
"python-embed\python.exe" -m pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location

echo.
echo 安装 openai-whisper / tiktoken ...
"python-embed\python.exe" -m pip install openai-whisper tiktoken -i https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location

echo.
echo 安装 numba 加速库 ...
"python-embed\python.exe" -m pip install numba -i https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location

echo.
echo 安装 pyinstaller 打包工具 ...
"python-embed\python.exe" -m pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location

echo.
echo ========================================
echo   依赖安装完成！
echo ========================================
echo.
pause