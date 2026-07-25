# AI视频字幕提取工具箱
自用Python字幕识别小工具，基于Whisper实现视频音频转字幕。

## 环境要求
1. Python 3.9+
2. AutoHotkey（运行 `gui.ahk` 图形辅助脚本）
3. 依赖库：见安装依赖.bat

## 首次部署步骤
1. 克隆本仓库到本地
2. 运行 `安装依赖.bat`，自动安装Python第三方库
3. 下载Whisper small模型 `small.pt`
   - 模型存放路径：`cache/` 文件夹
4. 双击 `启动工具.bat` 运行程序

## 文件说明
- `main.py`：程序主逻辑
- `batch_trans.py`：批量字幕处理功能
- `gui.ahk`：图形界面辅助脚本，直接双击运行
- `启动工具.bat`：调用本机Python启动项目
- `打包.bat`：PyInstaller打包脚本，可编译为独立exe
- `bin/`：ffmpeg运行必需程序

## 注意事项
1. 本仓库仅存放源代码，**不包含AI模型文件**，请自行下载模型放入cache目录。
2. 仓库不含打包产物（exe、内嵌Python环境等），换新电脑需要本地重新打包。
3. 模型来源：OpenAI Whisper官方项目。

## 打包
如需生成独立运行程序，配置好环境后直接运行 `打包.bat`，打包输出在dist目录。

### 打包好的版本前往release下载
