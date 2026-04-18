#!/bin/bash

echo "=== Avvio Magazzino Fermi ==="

# Avvia MySQL se non è già in esecuzione
if ! systemctl is-active --quiet mysql; then
    echo ">> Avvio MySQL..."
    sudo systemctl start mysql
else
    echo ">> MySQL già in esecuzione"
fi

# Attiva il venv e avvia Django in background
echo ">> Avvio server Django..."
cd ~/PyCharmMiscProject/SSH/BackEnd
source ../venv/bin/activate
fuser -k 8000/tcp 2>/dev/null  # killa eventuale processo già sulla porta
python3 manage.py runserver &
DJANGO_PID=$!

# Avvia il frontend in background
echo ">> Avvio Frontend..."
cd ~/PyCharmMiscProject/SSH/FrontEnd
fuser -k 5500/tcp 2>/dev/null
python3 -m http.server 5500 &
FRONTEND_PID=$!

echo ""
echo "=== Tutto avviato! ==="
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5500/Home.html"
echo ""
echo "Premi CTRL+C per fermare tutto"

# Aspetta e al CTRL+C ferma entrambi
trap "echo '>> Fermo tutto...'; kill $DJANGO_PID $FRONTEND_PID; exit" SIGINT SIGTERM
wait