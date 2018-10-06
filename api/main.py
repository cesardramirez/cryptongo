import pymongo
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

from agent import main as agent

app = Flask(__name__)


@app.route("/")
def index():
    """
    :return: Endpoints Cryptongo API
    """

    # jsonify: Convierte diccionarios de python al formato json.
    return jsonify(
        {
            'name': 'Cryprongo API',
            'index': request.host_url,
            'endpoint_1': request.host_url + 'top-rank-20',
            'endpoint_2': request.host_url + 'tickers'
        }
    )


def get_db_connection(uri):
    """
    Define la conexión a la BD.
    MongoClient por defecto se conecta al localhost.
    :param uri: URI de conexión.
    :return: BD a utilizar.
    """
    client = pymongo.MongoClient(uri)
    return client.cryptongo


db_connection = get_db_connection('mongodb://crypto-mongodb-dev:27017/')


@app.route('/tickers', methods=['GET'])
def get_documents():
    """
    Obtiene todos los documentos de la coleccion de la BD.
    :return: Una lista de los documentos según el criterio de búsqueda.
    """

    params = {}
    # request: Recibe la petición de la url y los parámetros (si tiene).
    name = request.args.get('name', '')  # Si no hay valor, será un str vacío.
    limit = int(request.args.get('limit', 0))

    if name:
        params.update({'name': name})  # Añade el valor al diccionario.

    # Se define que no se muestre los campos _id y ticker_hash.
    cursor = db_connection.tickers.find(params, {'_id': 0, 'ticker_hash': 0}).limit(limit)

    return jsonify(list(cursor))


@app.route("/top-rank-20", methods=['GET'])
def get_rank_top20():
    """
    Obtiene los documentos que tienen un ranking menor o igual a 20.
    :return: Una lista de los documentos según el criterio de búsqueda.
    """

    params = {}
    name = request.args.get('name', '')
    limit = int(request.args.get('limit', 0))

    if name:
        params.update({'name': name})

    params.update({'rank': {'$lte': 20}})

    cursor = db_connection.tickers.find(params, {'_id': 0, 'ticker_hash': 0}).limit(limit)

    return jsonify(list(cursor))


@app.route('/tickers', methods=['DELETE'])
def remove_currency():
    """
    Eliminar uno o varios documentos de la coleccion según el nombre de la criptomoneda.
    :return: La cantidad de documentos eliminados.
    """

    params = {}
    name = request.args.get('name', '')

    if name:
        params.update({'name': name})

        number = db_connection.tickers.delete_many(params).deleted_count

        if number > 0:
            message = 'Documentos eliminados'
            return jsonify(message=message, number=number), 200  # Ok
        else:
            error = 'No se encontraron documentos'
            return jsonify(error=error), 404  # Not Found
    else:
        error = 'No se envío el parámetro name'
        return jsonify(error=error), 400  # Bad Request


@app.route('/tickers', methods=['POST'])
def add_currency():
    try:
        data_request = request.get_json()

        if agent.save_ticker(db_connection, data_request):
            message = 'Documento almacenado exitosamente'
            return jsonify(message=message), 200
        else:
            error = 'El documento ya existe'
            return jsonify(error=error), 400
    except BadRequest:
        error = 'No se envío información en el body'
        return jsonify(error=error), 400
