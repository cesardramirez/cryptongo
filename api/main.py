import pymongo
from flask import Flask, request

app = Flask(__name__)

"""
jsonify: convierte diccionarios de python al formato json
request: recibe la peticion de la url y los parametros (si tiene)

"""

def get_db_connection(uri):
    """
    Define la conexión a la BD.
    MongoClient por defecto se conecta al localhost.
    :param uri: URI de conexión.
    :return: BD a utilizar.
    """
    client = pymongo.MongoClient(uri)
    return client.cryptongo


db_connection = get_db_connection('mongodb://localhost:27017/')


def get_documents():
    """
    Obtiene todos los documentos de la coleccion de la BD.
    :return: Una lista de los documentos según los parámetros definidos en el GET.
    """
    params = {}
    name = request.args.get('name', '')  # Si no hay valor, será un str vacío.
    limit = int(request.args.get('limit', 0))

    if name:
        params.update({'name': name})  # Añade el valor al diccionario.

    # Se define que no se muestre los campos _id y ticker_hash.
    cursor = db_connection.tickers.find(params, {'_id': 0, 'ticker_hash': 0}).limit(limit)

    return list(cursor)


def get_top20():
    """
    Obtiene los primeros 20 documentos.
    :return:
    """
    pass


def remove_currency():
    """
    Eliminar un documento de la coleccion.
    :return:
    """
    pass