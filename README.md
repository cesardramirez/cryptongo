## Descripción
Proyecto hecho con Python (3.5.2) y MongoDB (4.0.2)

## Endpoints

### Ticker
`GET /top-rank-20`
<br>Descripción: Obtiene los documentos que tienen un ranking menor o igual a 20.
- Parámetros opcionales:
  <br>(str) name - Busca por el nombre específico de una criptomoneda.
  <br>(int) limit - Cantidad máxima de resultados.
- Ejemplos:
  <br>[http://127.0.0.1:5000/top-rank-20](http://127.0.0.1:5000/top-rank-20)
  <br>[http://127.0.0.1:5000/top-rank-20?name=Bitcoin](http://127.0.0.1:5000/top-rank-20?name=Bitcoin)
  <br>[http://127.0.0.1:5000/top-rank-20?limit=5](http://127.0.0.1:5000/top-rank-20?limit=5)
  
  Respuesta Simple:
  ```json
  [
    {
      "circulating_supply": 17304600,
      "id": 1,
      "last_updated": 1538666489,
      "max_supply": 21000000,
      "name": "Bitcoin",
      "quotes": {
        "USD": {
          "market_cap": 113747701200,
          "percent_change_1h": -0.02,
          "percent_change_24h": 0.98,
          "percent_change_7d": 0.62,
          "price": 6573.26382583,
          "volume_24h": 3827024537.65621
        }
      },
      "rank": 1,
      "symbol": "BTC",
      "total_supply": 17304600,
      "website_slug": "bitcoin"
    }
  ]
  ```
    

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

Insertar información reciente en la Base de Datos

> Creará la colección insertando todas las criptomonedas existentes.
> <br>Si existen cambios en los campos 'last_updated' y 'quotes', insertará el documento.

    source venv/bin/activate
    python3 agent/main.py
    
Ejecutar el proyecto

>Por cada cambio en código se debe reiniciar el servidor.

    export FLASK_APP=api/main.py
    flask run

## Herramientas y bibliografía

* [Markown Live Preview](http://markdownlivepreview.com/)
* [JSON Formatter Chrome Extension](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa)
* [Coin Market Cap API](https://coinmarketcap.com/api/)