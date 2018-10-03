import pymongo
import requests

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

    # Obtiene la data de ticker y si encuentra un documento, retorna True para que no lo almacene.
    if db_connection.tickers.find_one({'ticker_hash': 'x'}):
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

    # Obtiene la data del ticker y la almacena en la BD de Mongo por medio de insertOne()
    db_connection.tickers.insert_one(ticker_data)
    return True
