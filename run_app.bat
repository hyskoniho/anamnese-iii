@echo off
REM Ativa o ambiente virtual e executa o __main__.py

REM Caminho para a venv
set VENV_DIR=.venv

REM Ativar a venv
call %VENV_DIR%\Scripts\activate.bat

REM Executar o programa principal
python src\__main__.py

REM Manter o terminal aberto após execução
pause
