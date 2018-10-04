## Descripción
Proyecto hecho con Python (3.5.2) y MongoDB (4.0.2)

## Instalación y ejecución
Ubuntu 16.x

    python3 -V
    wget https://bootstrap.pypa.io/get-pip.py -O ~/get-pip.py
    sudo python3 ~/get-pip.py
    sudo apt-get install python3-venv
    git clone https://github.com/cesardramirez/cryptongo.git
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

Opción alternativa (paquetes recientes)

    ...
    source venv/bin/activate
    pip install --upgrade pip
    pip install pymongo
    pip install flask
    pip install requests
    pip install pylint

Realizar backup a la Base de Datos

    mongodump --host localhost --port 27017 --out ~/backup_mongodb/backup-2018-10-04/ --collection tickers --db cryptongo

Restaurar la Base de Datos

    mongorestore --host localhost --port 27017 ~/backup_mongodb/backup-2018-10-04
    
Ejecutar el proyecto

>Por cada cambio en código se debe reiniciar el servidor.

    export FLASK_APP=api/main.py
    flask run

## Herramientas y bibliografía

* [Markown Live Preview](http://markdownlivepreview.com/)
* [JSON Formatter Chrome Extension](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa)
* [Coin Market Cap API](https://coinmarketcap.com/api/)