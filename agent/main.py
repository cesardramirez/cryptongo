import pymongo
import requests
from collections import OrderedDict
from hashlib import sha512

API_URL = 'https://api.coinmarketcap.com/v2/ticker/'


def get_db_connection(uri):
    """
    Define la conexión a la BD.
    MongoClient por defecto se conecta al localhost.
    :param uri: URI de conexión.
    :return: BD a utilizar.
    """
    client = pymongo.MongoClient(uri)
    return client.cryptongo


def get_hash(value):
    # Tomar el string y convertirlo en un hash con el sha-512
    return sha512(value.encode('utf-8')).hexdigest()


def first_element(elements):
    # Ordenamiento de la informacion y obtener el mismo string asi se lo pase varias veces.
    # elements va a ser una tupla con key, value
    # Se va a ordenar a traves de la key
    return elements[0]


def get_ticker_hash(ticker_data):
    # Obtiene todos los valores y lo coloca en un string largo.
    # TODO: Ver si los valores name, last_updated y price se repiten. Para ver si no existen conflictos al geneerar el hash.
    # TODO: Ver si se puede optimizar la funcion first_element, porque si solo trae la key, pues se puede colocar en el mismo ordenamiento.
    ticker_data = OrderedDict(sorted(ticker_data.items(), key=first_element))

    # TODO: Al parecer el hash lo crea concatenando todos los campos del documento ordenado por su key. Ver como optimizar esto.
    ticker_value = ''
    for value in ticker_data.values():
        ticker_value += str(value)

    return get_hash(ticker_value)


def get_cryptocurrencies_from_api():
    """
    De la API de CoinMarketCap obtiene todos los objetos.
    :return: Diccionario.
    """

    r = requests.get(API_URL)
    if r.status_code == 200:
        result = r.json()
        return result

    raise Exception('API Error')  # Lanzar una excepción.


def check_if_exists(db_connection, ticker_data):
    """
    Verifica si la información ya existe en la BD (por medio de un hash).
    :param db_connection:
    :param ticker_data:
    :return:
    """

    # TODO: Enviar como parametro el ticker_hash, para que no tenga que llamar a la funcion y llamarla nuevamente.
    ticker_hash = get_ticker_hash(ticker_data)

    # Obtiene la data de ticker y si encuentra un documento, retorna True para que no lo almacene.
    if db_connection.tickers.find_one({'ticker_hash': ticker_hash}):
        return True

    return False


def save_ticker(db_connection, ticker_data=None):
    """
    Almancenar el documento en la BD.
    Verificará si el documento ya existe para no almacenarlo nuevamente.
    :param db_connection:
    :param ticker_data:
    :return:
    """

    # Evita operaciones si no existe información.
    if not ticker_data:
        return False

    if check_if_exists(db_connection, ticker_data):
        return False

    # TODO: Ver como optimizar esto. Por cada vez que se llama get_ticker_hash lo va a ordenar y va a crear el hash.
    ticker_data['ticker_hash'] = get_ticker_hash(ticker_data)

    # Obtiene la data del ticker y la almacena en la BD de Mongo por medio de insertOne()
    db_connection.tickers.insert_one(ticker_data)
    return True
