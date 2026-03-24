#!/bin/bash

echo "=== Setup Magazzino Fermi ==="

# Installa dipendenze di sistema
sudo apt update -y
sudo apt install python3 python3-venv libmysqlclient-dev mysql-server -y

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
python3 -m pip install django djangorestframework mysqlclient channels djangorestframework-simplejwt django-cors-headers

# Migrate
cd BackEnd
python3 manage.py migrate

echo "=== Setup completato! ==="
echo "Ora lancia: python3 manage.py createsuperuser"