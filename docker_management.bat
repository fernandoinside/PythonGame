@echo off
title Docker Management Script
setlocal EnableDelayedExpansion

:: Define o nome padrão do ambiente
set last_env=AppGame
echo AppGame > last_environment.txt

:menu
cls
echo ============================
echo Docker Management Script
echo ============================
echo.
if defined last_env (
    echo Usando ambiente: !last_env!
) else (
    echo Nenhum ambiente encontrado.
)
echo.
echo Escolha uma opcao:
echo.
echo 1) Criar Novo Ambiente
echo    Significa: Cria uma nova imagem e container com o nome especificado.
echo.
echo 2) Subir Container
echo    Comando: docker build -t !last_env! .
echo    Significa: Constroi uma imagem Docker a partir do Dockerfile no diretorio atual.
echo.
echo 3) Subir Docker Compose
echo    Comando: docker-compose up -d
echo    Significa: Sobe todos os servicos definidos no arquivo docker-compose.yml em background.
echo.
echo 4) Derrubar Docker Compose
echo    Comando: docker-compose down
echo    Significa: Derruba todos os servicos definidos no arquivo docker-compose.yml.
echo.
echo 5) Ver Logs do Container
echo    Comando: docker logs !last_env!
echo    Significa: Exibe os logs do container especificado.
echo.
echo 6) Parar Container
echo    Comando: docker stop !last_env!
echo    Significa: Para o container especificado.
echo.
echo 7) Remover Container
echo    Comando: docker rm !last_env!
echo    Significa: Remove o container especificado.
echo.
echo 8) Adicionar Serviço
echo    Adiciona um novo serviço ao container.
echo.
echo 9) Atualizar Aplicação Python
echo    Atualiza a aplicação Python no container.
echo.
echo 10) Visualizar Aplicação Python
echo    Visualiza a aplicação Python no container.
echo.
echo 11) Automático: Criar e Subir Aplicação
echo    Cria o ambiente, sobe o Docker Compose, atualiza a aplicação Python e mostra o endereço da aplicação.
echo.
echo 12) Ajuda
echo    Descreve as ferramentas instaladas e como usá-las.
echo.
echo 13) Sair
echo.

set /p escolha=Digite sua opcao (1-13): 

if "%escolha%"=="1" goto create_environment
if "%escolha%"=="2" goto build_image
if "%escolha%"=="3" goto compose_up
if "%escolha%"=="4" goto compose_down
if "%escolha%"=="5" goto view_logs
if "%escolha%"=="6" goto stop_container
if "%escolha%"=="7" goto remove_container
if "%escolha%"=="8" goto add_service
if "%escolha%"=="9" goto update_python_app
if "%escolha%"=="10" goto view_python_app
if "%escolha%"=="11" goto automatic
if "%escolha%"=="12" goto help
if "%escolha%"=="13" goto end
goto menu

:create_environment
echo.
set /p new_env=Digite o nome do novo ambiente: 
echo !new_env! > last_environment.txt
set last_env=!new_env!
echo Ambiente "!new_env!" criado e salvo.
pause
goto menu

:build_image
if not defined last_env (
    echo Nenhum ambiente configurado. Por favor, crie um novo ambiente primeiro.
    pause
    goto menu
)
echo.
echo ============================
echo Subir Container
echo ============================
docker build -t !last_env! .
echo.
pause
goto menu

:compose_up
if not defined last_env (
    echo Nenhum ambiente configurado. Por favor, crie um novo ambiente primeiro.
    pause
    goto menu
)
echo.
echo ============================
echo Subir Docker Compose
echo ============================
docker-compose up -d
echo.
pause
goto menu

:compose_down
if not defined last_env (
    echo Nenhum ambiente configurado. Por favor, crie um novo ambiente primeiro.
    pause
    goto menu
)
echo.
echo ============================
echo Derrubar Docker Compose
echo ============================
docker-compose down
echo.
pause
goto menu

:view_logs
if not defined last_env (
    echo Nenhum ambiente configurado. Por favor, crie um novo ambiente primeiro.
    pause
    goto menu
)
echo.
echo ============================
echo Ver Logs do Container
echo ============================
docker logs !last_env!
echo.
pause
goto menu

:stop_container
if not defined last_env (
    echo Nenhum ambiente configurado. Por favor, crie um novo ambiente primeiro.
    pause
    goto menu
)
echo.
echo ============================
echo Parar Container
echo ============================
docker stop !last_env!
echo.
pause
goto menu

:remove_container
if not defined last_env (
    echo Nenhum ambiente configurado. Por favor, crie um novo ambiente primeiro.
    pause
    goto menu
)
echo.
echo ============================
echo Remover Container
echo ============================
docker rm !last_env!
echo.
pause
goto menu

:add_service
echo.
echo Escolha um serviço para adicionar:
echo.
echo 1) Instalar Nginx
echo 2) Instalar Apache
echo 3) Instalar Bibliotecas de IA (numpy, pandas, scipy, scikit-learn, tensorflow, keras)
echo 4) Instalar Wifite
echo.
set /p service_option=Digite sua opcao (1-4): 

if "%service_option%"=="1" goto install_nginx
if "%service_option%"=="2" goto install_apache
if "%service_option%"=="3" goto install_ia
if "%service_option%"=="4" goto install_wifite
goto add_service

:install_nginx
docker exec -it !last_env! sh -c "apk update && apk add --no-cache nginx && rc-service nginx start"
echo Nginx instalado e iniciado.
pause
goto menu

:install_apache
docker exec -it !last_env! sh -c "apk update && apk add --no-cache apache2 && rc-service apache2 start"
echo Apache instalado e iniciado.
pause
goto menu

:install_ia
docker exec -it !last_env! sh -c "pip install numpy pandas scipy scikit-learn tensorflow keras"
echo Bibliotecas de IA instaladas.
pause
goto menu

:install_wifite
docker exec -it !last_env! sh -c "apk update && apk add --no-cache wifite"
echo Wifite instalado.
pause
goto menu

:update_python_app
if not defined last_env (
    echo Nenhum ambiente configurado. Por favor, crie um novo ambiente primeiro.
    pause
    goto menu
)
docker cp ./PythonGame !last_env!:/app
docker exec -it !last_env! sh -c "cd /app && pip install -r requirements.txt"
echo Aplicacao Python atualizada no container.
pause
goto menu

:view_python_app
if not defined last_env (
    echo Nenhum ambiente configurado. Por favor, crie um novo ambiente primeiro.
    pause
    goto menu
)
docker exec -it !last_env! sh -c "cd /app && python app.py"
pause
goto menu

:automatic
docker-compose down
docker-compose up -d --build
docker cp ./PythonGame AppGame:/app
docker exec -it AppGame sh -c "cd /app && pip install -r requirements.txt"
echo Aplicacao Python atualizada no container.
echo.
echo Acesse a aplicacao em http://localhost:5000
pause
goto menu

:help
echo.
echo ============================
echo Ajuda
echo ============================
type README.md
echo.
pause
goto menu

:end
echo Saindo...
exit
