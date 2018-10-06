import pymongo
import requests
from collections import OrderedDict
from hashlib import sha512

API_URL = 'https://api.coinmarketcap.com/v2/ticker/'
API_URL_START = 'https://api.coinmarketcap.com/v2/ticker/?start={}'
API_URL_LISTINGS = 'https://api.coinmarketcap.com/v2/listings/'


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
    """
    :param value: String con todos los valores de los campos del documento concatenados.
    :return: String hash generado con sha-512.
    """
    return sha512(value.encode('utf-8')).hexdigest()


def field_name(field):
    """
    :param field: Tupla que tiene el nombre y valor de un campo del documento original.
    :return: El nombre del campo.
    """
    return field[0]


def remove_element_dictionary(dictionary, key):
    """
    Un diccionario puede ser dinámico, por lo cuál se utiliza este método para eliminar un elemento del mismo.
    :param dictionary:
    :param key:
    :return: Diccionario con el elemento eliminado.
    """

    r = dict(dictionary)
    del r[key]
    return r


def get_ticker_hash(ticker_data):
    """
    Genera el hash a partir de cada uno de los valores del documento.
    El documento (o diccionario) será ordenado alfabéticamente según su key.
    Como no se está ordenando los elementos del subdocumento 'quotes' se elimina temporalmente del diccionario
    para no tenerlo en cuenta al momento de la creación del hash.
    Si existe un valor diferente para el campo last_updated indica que los valores del subdocumento quotes también
      cambió, por lo cuál este documento será almacenado posteriormente en la BD.
    :param ticker_data: Documento de la criptomoneda.
    :return: La función que genera el hash según el string con todos los valores del documento concatenados.
    """

    ticker_data = remove_element_dictionary(ticker_data, 'quotes')
    ticker_data = OrderedDict(sorted(ticker_data.items(), key=field_name))

    # Se concatena en un string todos los valores ordenados del diccionario.
    ticker_value = ''
    for _, value in ticker_data.items():
        ticker_value += str(value)

    return get_hash(ticker_value)


def get_cryptocurrencies_from_api(position):
    """
    De la API de CoinMarketCap se obtiene los documentos desde una posición inicial.
      La API por cada endpoint sólo permite 100 documentos.
    :return: Resultado de la consulta en formato json.
    """

    url = API_URL_START.format(position)

    r = requests.get(url)
    if r.status_code == 200:
        result = r.json()
        return result

    raise Exception('API Error')  # Lanzar una excepción.


def get_num_cryptocurrencies_from_api():
    """
    De la API de CoinMarketCap se obtiene la cantidad de criptomonedas existentes.
    :return: Valor entero con la cantidad de documentos.
    """

    r = requests.get(API_URL_LISTINGS)
    if r.status_code == 200:
        result = r.json()
        return result['metadata']['num_cryptocurrencies']

    raise Exception('API Error')


def check_if_exists(db_connection, ticker_hash):
    """
    Verifica si la información ya existe en la BD (por medio de un hash).
    La BD almacenará un historico de las criptomonedas.
    :param db_connection: Conexión a la BD.
    :param ticker_hash: Hash del documento generado previamente.
    :return: Verdadero si el documento ya se encuentra, Falso si no.
    """

    if db_connection.tickers.find_one({'ticker_hash': ticker_hash}):
        return True

    return False


def save_ticker(db_connection, ticker_data=None):
    """
    Almacena el documento en la BD siempre y cuando no exista.
    Se identifica si el documento ya fue almacenado o no por la generación de un hash.
    :param db_connection:
    :param ticker_data: Datos del documento.
    :return: Verdadero si almacena el documento.
    """

    # Evita operaciones si no existe información.
    if not ticker_data:
        return False

    ticker_hash = get_ticker_hash(ticker_data)

    if check_if_exists(db_connection, ticker_hash):
        return False

    ticker_data['ticker_hash'] = ticker_hash

    # Almacena el documento en la BD de Mongo por medio de insertOne()
    db_connection.tickers.insert_one(ticker_data)

    return True


if __name__ == '__main__':
    """
    Para crear la conexión ssh del contenedor de Docker,
      es necesario que el programa inicialmente se este ejecutando contantemente.
    import time
    while True:
        time.sleep(300)
    """

    connection = get_db_connection('mongodb://crypto-mongodb-dev:27017/')
    num_cryptocurrencies = get_num_cryptocurrencies_from_api()
    print('\nCryptomonedas actuales en Coin Market Cap: {}'.format(num_cryptocurrencies))

    cont = 0
    for i in range(1, num_cryptocurrencies, 100):

        tickers = get_cryptocurrencies_from_api(i)
        tickers_data = tickers['data']

        for value in tickers_data.values():
            if save_ticker(connection, value):
                cont += 1

        print('Tickers almacenados... {}'.format(cont)) if cont > 0 else print('...')

    print('\nCryptomonedas totales almacenadas: {}'.format(cont))
