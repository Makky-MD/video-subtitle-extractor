#SingleInstance Force
Gui +LastFound
Gui Add, Button, x45 y40 w150 h35 gBtnStart, 开始生成字幕
Gui Add, Button, x45 y90 w150 h35 gBtnHelp, 查看使用说明
Gui Show, w240 h170, AI字幕工具箱
return

BtnStart:
Run, .\启动工具.bat
return

BtnHelp:
Run, .\使用说明.txt
return