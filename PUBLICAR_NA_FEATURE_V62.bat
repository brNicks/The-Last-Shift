@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
echo =============================================
echo THE LAST SHIFT - V62 - PUBLICAR SOMENTE FEATURE

echo =============================================
where git >nul 2>&1
if errorlevel 1 (
    echo Git nao encontrado. Instale Git for Windows primeiro.
    pause
    exit /b 1
)
where powershell.exe >nul 2>&1
if errorlevel 1 (
    echo PowerShell nao encontrado. Requer Windows 10/11 com PowerShell habilitado.
    echo Nenhuma alteracao foi publicada.
    pause
    exit /b 1
)
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%~dp0VERIFICAR_PACOTE.ps1"
if errorlevel 1 (
    echo O verificador de integridade falhou. A publicacao foi cancelada.
    pause
    exit /b 1
)
set "TARGET=%~dp0_GITHUB_PREPARACAO_V62"
set "REMOTE=https://github.com/brNicks/The-Last-Shift.git"
if not exist "%TARGET%\.git" (
    if exist "%TARGET%" (
        echo A pasta de clone existe, mas nao parece ser um repositorio Git.
        echo Renomeie essa pasta e tente novamente.
        pause
        exit /b 1
    )
    git clone --branch feature/sprites-v62 --single-branch "%REMOTE%" "%TARGET%"
    if errorlevel 1 (
        echo Nao foi possivel obter a branch feature/sprites-v62.
        pause
        exit /b 1
    )
)
for /f "delims=" %%B in ('git -C "%TARGET%" branch --show-current') do set "CURRENT_BRANCH=%%B"
if /I not "%CURRENT_BRANCH%"=="feature/sprites-v62" (
    echo ERRO: branch inesperada: %CURRENT_BRANCH%
    echo Nenhuma alteracao foi publicada.
    pause
    exit /b 1
)
for /f "delims=" %%R in ('git -C "%TARGET%" remote get-url origin') do set "ACTUAL_REMOTE=%%R"
if /I not "%ACTUAL_REMOTE%"=="%REMOTE%" (
    echo ERRO: remoto inesperado: %ACTUAL_REMOTE%
    echo Para evitar publicar no repositorio errado, operacao cancelada.
    pause
    exit /b 1
)
set "DIRTY="
for /f "delims=" %%S in ('git -C "%TARGET%" status --porcelain') do set "DIRTY=1"
if defined DIRTY (
    echo Ha alteracoes preexistentes na pasta de preparacao. Revise antes de continuar.
    pause
    exit /b 1
)
git -C "%TARGET%" pull --ff-only origin feature/sprites-v62
if errorlevel 1 (
    echo Nao foi possivel atualizar a branch com seguranca.
    pause
    exit /b 1
)
robocopy "%~dp0baldisoffice" "%TARGET%\baldisoffice" /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 (
    echo Erro ao copiar arquivos do jogo.
    pause
    exit /b 1
)
robocopy "%~dp0TESTES_OPCIONAIS" "%TARGET%\TESTES_OPCIONAIS" /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 (
    echo Erro ao copiar testes opcionais.
    pause
    exit /b 1
)
for %%F in (README.md requirements.txt EXECUTAR_NO_WINDOWS.bat .gitignore CHANGELOG_V62.md CHECKLIST_FASE1_FINAL.md GITHUB_PUBLICACAO.md VERIFICAR_PROJETO.py VERIFICAR_PACOTE.ps1 MANIFEST_SHA256.txt PUBLICAR_NA_FEATURE_V62.bat) do (
    copy /Y "%~dp0%%F" "%TARGET%\%%F" >nul
    if errorlevel 1 (
        echo Falha ao copiar %%F
        pause
        exit /b 1
    )
)
git -C "%TARGET%" add -- baldisoffice TESTES_OPCIONAIS README.md requirements.txt EXECUTAR_NO_WINDOWS.bat .gitignore CHANGELOG_V62.md CHECKLIST_FASE1_FINAL.md GITHUB_PUBLICACAO.md VERIFICAR_PROJETO.py VERIFICAR_PACOTE.ps1 MANIFEST_SHA256.txt PUBLICAR_NA_FEATURE_V62.bat
if errorlevel 1 (
    echo Falha ao preparar o commit.
    pause
    exit /b 1
)
git -C "%TARGET%" diff --cached --stat

git -C "%TARGET%" diff --cached --quiet
if not errorlevel 1 (
    echo Nao ha alteracoes novas para publicar.
    pause
    exit /b 0
)
echo.
echo ATENCAO: o commit sera enviado SOMENTE para feature/sprites-v62.
echo Branch main NAO sera alterada.
choice /C SN /M "Confirmar commit e push para feature/sprites-v62"
if errorlevel 2 (
    echo Publicacao cancelada.
    pause
    exit /b 0
)
git -C "%TARGET%" commit -m "V62: consolidar Fase 1 aprovada"
if errorlevel 1 (
    echo Erro ao criar commit. Confira nome e email do Git.
    pause
    exit /b 1
)
git -C "%TARGET%" push origin feature/sprites-v62
if errorlevel 1 (
    echo Falha no push. O commit ficou salvo somente na pasta de preparacao.
    pause
    exit /b 1
)
echo.
echo Publicacao na branch feature/sprites-v62 concluida.
echo Confira: https://github.com/brNicks/The-Last-Shift/tree/feature/sprites-v62
pause
endlocal
