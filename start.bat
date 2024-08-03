@echo off
REM Instalar Virtualenv
pip install virtualenv

REM Navegar até o diretório do projeto
cd /d %~dp0

REM Remover ambiente virtual existente (se houver)
IF EXIST venv (
    rmdir /s /q venv
)

REM Criar o ambiente virtual
python -m venv venv

REM Ativar o ambiente virtual
call venv\Scripts\activate

REM Atualizar o pip
python -m pip install --upgrade pip

REM Instalar as dependências
pip install -r requirements.txt

REM Executar a aplicação Flask
python app.py

pause