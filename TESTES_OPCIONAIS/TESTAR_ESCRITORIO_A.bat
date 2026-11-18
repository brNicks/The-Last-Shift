@echo off
cd /d "%~dp0..\baldisoffice"
py -m pip install -r "%~dp0..\requirements.txt"
py testar_escritorio_a.py
pause
