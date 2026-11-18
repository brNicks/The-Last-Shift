@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado. Instale Python 3 e habilite o comando py.
    pause
    exit /b 1
)
py -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencia pygame...
    py -m pip install -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo Nao foi possivel instalar pygame. Verifique a conexao.
        pause
        exit /b 1
    )
)
cd /d "%~dp0baldisoffice"
py main.py
if errorlevel 1 (
    echo.
    echo O jogo encerrou com erro. Envie uma captura desta janela.
    pause
    exit /b 1
)
pause
endlocal
