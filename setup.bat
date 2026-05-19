@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Setup Magazzino Fermi - Windows
echo ============================================
echo.

:: ─── Controllo Python ───────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato nel PATH.
    echo Scaricalo da https://www.python.org/downloads/
    echo Assicurati di spuntare "Add Python to PATH" durante l'installazione.
    pause
    exit /b 1
)
echo [OK] Python trovato.

:: ─── Posizione progetto ─────────────────────────────────────────────────────
:: Imposta il percorso della cartella del progetto (quella che contiene BackEnd/)
set "PROJECT_DIR=%~dp0"
echo [INFO] Cartella progetto: %PROJECT_DIR%

:: ─── Creazione Virtual Environment ──────────────────────────────────────────
if not exist "%PROJECT_DIR%venv\" (
    echo [INFO] Creo il virtual environment...
    python -m venv "%PROJECT_DIR%venv"
    if errorlevel 1 (
        echo [ERRORE] Impossibile creare il venv.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment creato.
) else (
    echo [OK] Virtual environment gia' esistente.
)

:: ─── Attivazione venv ───────────────────────────────────────────────────────
call "%PROJECT_DIR%venv\Scripts\activate.bat"
echo [OK] Virtual environment attivato.

:: ─── Installazione dipendenze ───────────────────────────────────────────────
echo [INFO] Installo le dipendenze Python...
pip install --upgrade pip --quiet
pip install -r "%PROJECT_DIR%requirements.txt"
if errorlevel 1 (
    echo [ERRORE] Installazione dipendenze fallita.
    pause
    exit /b 1
)
echo [OK] Dipendenze installate.

:: ─── Controllo MySQL ────────────────────────────────────────────────────────
echo.
echo [INFO] Verifico MySQL...
mysql --version >nul 2>&1
if errorlevel 1 (
    echo [ATTENZIONE] MySQL non trovato nel PATH.
    echo Scarica MySQL Community Server da:
    echo   https://dev.mysql.com/downloads/mysql/
    echo Dopo l'installazione, aggiungi C:\Program Files\MySQL\MySQL Server X.X\bin al PATH
    echo e rilancia questo script.
    pause
    exit /b 1
)
echo [OK] MySQL trovato.

:: ─── Creazione database ─────────────────────────────────────────────────────
echo [INFO] Creo il database (se non esiste)...
mysql -u root -ppassword -e "CREATE DATABASE IF NOT EXISTS magazzino_fermi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul
if errorlevel 1 (
    echo [ATTENZIONE] Impossibile creare il database automaticamente.
    echo Apri MySQL Workbench o il prompt MySQL e lancia:
    echo   CREATE DATABASE IF NOT EXISTS magazzino_fermi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    echo Poi premi un tasto per continuare...
    pause
)

:: ─── Migrate ────────────────────────────────────────────────────────────────
echo [INFO] Eseguo le migrazioni Django...
cd "%PROJECT_DIR%BackEnd"
python manage.py migrate
if errorlevel 1 (
    echo [ERRORE] Migrate fallita. Controlla la connessione a MySQL e le credenziali in settings.py.
    pause
    exit /b 1
)
echo [OK] Database pronto.

:: ─── Fine ───────────────────────────────────────────────────────────────────
echo.
echo ============================================
echo   Setup completato con successo!
echo ============================================
echo.
echo Prossimi passi:
echo   1. Crea il superuser:
echo      python manage.py createsuperuser
echo.
echo   2. Avvia il server:
echo      python manage.py runserver
echo.
echo   (Il venv e' gia' attivo in questa finestra)
echo.
pause
