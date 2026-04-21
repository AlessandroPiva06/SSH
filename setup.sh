#!/bin/bash

echo "=== Setup Magazzino Fermi ==="

# Installa dipendenze di sistema
sudo apt update -y
sudo apt install python3 python3-venv python3-pip libmysqlclient-dev mysql-server -y

# Avvia MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Fix accesso MySQL
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password'; FLUSH PRIVILEGES;"

# Crea database
sudo mysql -u root -ppassword -e "CREATE DATABASE IF NOT EXISTS magazzino_fermi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Vai nella root del progetto
cd ~/PycharmProjects/SSH

# Ricrea venv pulito con --copies (evita problemi di symlink su Ubuntu/Debian)
rm -rf venv
python3 -m venv venv --copies

# Installa librerie Python usando il pip del venv direttamente
venv/bin/pip install --upgrade pip

venv/bin/pip install \
    django \
    djangorestframework \
    djangorestframework-simplejwt \
    django-cors-headers \
    channels \
    mysqlclient \
    python-decouple \
    django-filter \
    Pillow

# Crea .env se non esiste
if [ ! -f BackEnd/.env ]; then
    echo "SECRET_KEY=cambia-questa-chiave-segreta" > BackEnd/.env
    echo "DB_NAME=magazzino_fermi" >> BackEnd/.env
    echo "DB_USER=root" >> BackEnd/.env
    echo "DB_PASSWORD=password" >> BackEnd/.env
    echo "DB_HOST=localhost" >> BackEnd/.env
    echo "DB_PORT=3306" >> BackEnd/.env
    echo "⚠️  Creato BackEnd/.env — ricordati di cambiare la SECRET_KEY!"
fi

# Migrate
venv/bin/python3 BackEnd/manage.py migrate

echo ""
echo "=== Setup completato! ==="
echo ""
echo "Per avviare il server:"
echo "  venv/bin/python3 BackEnd/manage.py runserver"
echo ""
echo "Per creare il superuser:"
echo "  venv/bin/python3 BackEnd/manage.py createsuperuser"