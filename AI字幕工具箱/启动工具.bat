@echo off
chcp 65001 >nul
title AI字幕工具箱

:: 跳转到脚本所在目录
cd /d "%~dp0"
:: 将当前目录加入Python模块搜索路径，解决找不到batch_trans问题
set PYTHONPATH=%~dp0;%PYTHONPATH%

:: ===== 文件完整性校验 =====
if not exist "main.py" (
    echo ========================================
    echo  【错误】缺少 main.py 文件
    echo  请确认压缩包解压完整，不要删除任何文件
    echo  如仍有问题，请重新解压
    echo ========================================
    pause
    exit /b 1
)

if not exist "config.ini" (
    echo ========================================
    echo  【错误】缺少 config.ini 配置文件
    echo  请确认压缩包解压完整
    echo ========================================
    pause
    exit /b 1
)

if not exist "bin\ffmpeg.exe" (
    echo ========================================
    echo  【错误】缺少 bin\ffmpeg.exe
    echo  请确认 bin 文件夹完整
    echo ========================================
    pause
    exit /b 1
)

::if not exist "python-embed\python.exe" (
::   echo ========================================
::    echo  【错误】缺少 python-embed\python.exe
::    echo  请确认 python-embed 文件夹完整
::    echo ========================================
::    pause
::    exit /b 1
::)

:: ===== 启动主程序 =====
::"python-embed\python.exe" main.py
python main.py
pause