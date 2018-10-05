db.tickers.find({})
db.tickers.findOne({})
db.tickers.drop()

/* Cuenta cuantos documentos hay en una coleccion. */
db.tickers.count()
/* Muestra los valores unicos de un campo por todos los documentos.
  Si la cantidad es menor al numero de documentos en total, indica que hay valores repetidos.
*/
db.tickers.distinct('name')

db.tickers.distinct('circulating_supply')  // 1585
db.tickers.distinct('id')  // 2023
db.tickers.distinct('last_updated')  // 239
db.tickers.distinct('max_supply')  // 187
db.tickers.distinct('name')  // 2023
db.tickers.distinct('rank')  // 2023
db.tickers.distinct('symbol') // 1956
db.tickers.distinct('total_supply')  // 1425
db.tickers.distinct('website_slug')  // 2023

/* Filtra los documentos que tenga como nombre 'Bitcoin' y trae solo el valor 'price' del subdocumento 'quotes' */
db.tickers.find({name: 'Bitcoin'}, {'quotes.USD.price': 1})
db.tickers.find({name: 'Nxt'})

db.tickers.find({rank: {$lte: 20}})