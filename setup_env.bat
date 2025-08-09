@echo off

REM Ajuste esse caminho para o seu Python 3.13 instalado:
set PYTHON_EXE=C:\Users\Diego\AppData\Local\Programs\Python\Python313\python.exe

IF NOT EXIST venv (
    echo Criando ambiente virtual...
    "%PYTHON_EXE%" -m venv venv
) ELSE (
    echo Ambiente virtual ja existe.
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Atualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias...
pip install -r requirements.txt

echo Ambiente pronto! O ambiente virtual está ativado.
cmd /k
