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
    :return:
    """
    r = requests.get(API_URL)
    if r.status_code == 200:
        result = r.json()
        return result

    raise Exception('API Error')  # Lanzar una excepción.
