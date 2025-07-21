@echo off
echo ========================================
echo    OBS Auto Recorder - Instalador
echo ========================================
echo.

echo Verificando se Python esta instalado...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.7 ou superior
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para executar o programa:
echo   python obs_auto_recorder.py
echo.
echo Lembre-se de configurar o OBS WebSocket:
echo   1. Abra o OBS Studio
echo   2. Vá em Ferramentas > WebSocket Server Settings
echo   3. Configure a porta 4455
echo   4. Desmarque "Enable Authentication"
echo.
pause 