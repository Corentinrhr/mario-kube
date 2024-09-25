#!/bin/bash

if ! command -v mysql &> /dev/null; then
    echo "Le client MySQL n'est pas installe. Veuillez l'installer et reessayer."
    exit 1
fi

mysql -h 172.255.0.4 -P 3306 -u root -p'FISA_hcajbjaibh672983' -e "SELECT 1;" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "MariaDB est pret."
    exit 0
else
    echo "MariaDB n'est pas pret."
    exit 1
fi
