@echo off
:: Avvia il server Django su Windows

set "PROJECT_DIR=%~dp0"

:: Attiva il venv
call "%PROJECT_DIR%venv\Scripts\activate.bat"

:: Vai nella cartella BackEnd e avvia
cd "%PROJECT_DIR%BackEnd"
echo [INFO] Server in partenza su http://127.0.0.1:8000/
python manage.py runserver
