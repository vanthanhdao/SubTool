@echo off
echo === Building Python to EXE ===
pyinstaller --name="AITranslator" --windowed --onefile --icon=icon.ico main.py

echo === Building Installer with Inno Setup ===
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

pause
