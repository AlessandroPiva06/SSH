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

# Crea venv
cd ~/PyCharmMiscProject/SSH
python3 -m venv venv
source venv/bin/activate

# Installa librerie Python
pip install --upgrade pip

pip install \
    django \
    djangorestframework \
    djangorestframework-simplejwt \
    django-cors-headers \
    django-channels \
    channels \
    mysqlclient \
    python-decouple \
    Pillow \
    django-filter

# Copia .env di esempio se non esiste
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
cd BackEnd
python3 manage.py migrate

echo ""
echo "=== Setup completato! ==="
echo "Ora lancia: python3 BackEnd/manage.py createsuperuser"
echo "Poi avvia il server con: python3 BackEnd/manage.py runserver"