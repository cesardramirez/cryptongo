## Descripción
Proyecto hecho con Python (3.5.3) y MongoDB (4.0.3)

## Endpoints

### Ticker
`GET /tickers`
<br>Descripción: Obtiene todas las criptomonedas.
- Parámetros opcionales:
  <br>(string) name - Busca por el nombre específico de una criptomoneda.
  <br>(int) limit - Cantidad máxima de resultados.
- Ejemplos:
  <br>[http://127.0.0.1:5000/tickers](http://127.0.0.1:5000/tickers)
  <br>[http://127.0.0.1:5000/tickers?name=Bitcoin](http://127.0.0.1:5000/tickers?name=Bitcoin)
  <br>[http://127.0.0.1:5000/tickers?limit=10&name=Bitcoin](http://127.0.0.1:5000/tickers?limit=10&name=Bitcoin)

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

`GET /top-rank-20`
<br>Descripción: Obtiene las criptomonedas que tienen un ranking menor o igual a 20.
- Parámetros opcionales:
  <br>(string) name - Busca por el nombre específico de una criptomoneda.
  <br>(int) limit - Cantidad máxima de resultados.
- Ejemplos:
  <br>[http://127.0.0.1:5000/top-rank-20](http://127.0.0.1:5000/top-rank-20)
  <br>[http://127.0.0.1:5000/top-rank-20?name=Bitcoin](http://127.0.0.1:5000/top-rank-20?name=Bitcoin)
  <br>[http://127.0.0.1:5000/top-rank-20?limit=5](http://127.0.0.1:5000/top-rank-20?limit=5)

`DELETE /tickers?name=<nombre>`
<br>Descripción: Elimina una criptomoneda según el nombre enviado.
- Parámetros opcionales:
  <br>(string) name - Busca por el nombre específico de una criptomoneda.
- Ejemplo:
  <br>[http://127.0.0.1:5000/tickers?name=Bitcoin](http://127.0.0.1:5000/tickers?name=Bitcoin)
- Respuestas:
  <pre>Status: 200 OK
  { "message": "Documentos eliminados", "number": 3 }</pre>
  <pre>Status: 404 NOT FOUND
  { "error": "No se encontraron documentos" }
  </pre>
  <pre>Status: 400 BAD REQUEST
  { "error": "No se envío el parámetro name" }
  </pre>

`POST /tickers`
<br>Descripción: Inserta una criptomoneda.
- Ejemplo:
  <br>[http://127.0.0.1:5000/tickers](http://127.0.0.1:5000/tickers)
- Cuerpo:
  ```json
  {
    "circulating_supply": 102378911,
    "id": 1027,
    "last_updated": 1538734480,
    "max_supply": null,
    "name": "Ethereum",
    "quotes": {
      "USD": {
        "market_cap": 22675297167,
        "percent_change_1h": 0.15,
        "percent_change_24h": -1.07,
        "percent_change_7d": -2.43,
        "price": 221.484063947,
        "volume_24h": 1478256834.01358
      }
    },
    "rank": 2,
    "symbol": "ETH",
    "total_supply": 102378911,
    "website_slug": "ethereum"
  }
  ```
- Respuestas:
  <pre>Status: 200 OK
  { "message": "Documento almacenado exitosamente" }</pre>
  <pre>Status: 404 BAD REQUEST
  { "error": "El documento ya existe" }
  { "error": "No se envío información en el body" }
  </pre>


## Docker - Instalación y ejecución
> Revisar que hace cada instrucción en el archivo [**Makefile**](https://github.com/cesardramirez/cryptongo/blob/master/Makefile)

1. Obtener las imágenes necesarias de Docker Hub.
<br>`make get-images`
2. Crear la red.
<br>`make create-network`
3. Construir las imágenes por medio del Dockerfile
<br>`make build-development`
4. Crear e inicia los contenedores por medio del docker-compose.yml
<br>`make start-development`

#### Opcional
- Detiene los contenedores.
<br>`make stop-development`
- Restaura por medio del backup la BD de Mongo.
<br>`make load-mongo`

### Comandos Docker
- Ingresar a los contenedores
<br>`docker exec -it crypto-mongodb-dev bash`
<br>`docker exec -it crypto-agent-dev bash`
- Eliminar los contenedores
<br>`docker rm -f crypto-mongodb-dev crypto-agent-dev`
<br>`docker rm -f $(docker ps -qa)`
- Visualizar los logs de un servicio específico
<br>`docker-compose logs agent`
<br>`docker logs -f crypto-agent-dev`
- Eliminar todas las imagenes
<br>`docker rmi -f $(docker images -q)`


## Virtualenv - Instalación y ejecución
Ubuntu 16.x

    python3 -V
    wget https://bootstrap.pypa.io/get-pip.py -O ~/get-pip.py
    sudo python3 ~/get-pip.py
    sudo apt-get install python3-venv
    git clone https://github.com/cesardramirez/cryptongo.git
    cd cryptongo
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

    mongodump --host localhost --port 27017 --out backup_bd/backup-2018-10-04 --collection tickers --db cryptongo

Restaurar la Base de Datos

    mongorestore --host localhost --port 27017 backup_bd/backup-2018-10-04

Insertar información reciente en la Base de Datos por medio de la API

> Creará la colección insertando todas las criptomonedas existentes de Coin Market Cap.
> <br>Si existen cambios en los campos 'last_updated' y 'quotes', insertará el documento.

    source venv/bin/activate
    python3 agent/main.py
    
Ejecutar el proyecto

>Por cada cambio en código se debe reiniciar el servidor.

    export FLASK_APP=api/main.py
    flask run


## Herramientas y bibliografía

* [Markown Live Preview](http://markdownlivepreview.com/)
* [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
* [JSON Formatter Chrome Extension](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa)
* [API Coin Market Cap](https://coinmarketcap.com/api/)
* [Wiki Cryptongo](https://github.com/cesardramirez/cryptongo/wiki)