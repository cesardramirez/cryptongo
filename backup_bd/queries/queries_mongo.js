/* Para los documentos se obtiene la información en https://api.coinmarketcap.com/v2/ticker/1/ */

/* Define una variable */
documento1 = {
    "id": 1,
    "name": "Bitcoin", 
    "symbol": "BTC", 
    "website_slug": "bitcoin", 
    "rank": 1, 
    "circulating_supply": 17298637.0, 
    "total_supply": 17298637.0, 
    "max_supply": 21000000.0, 
    "quotes": {
        "USD": {
            "price": 6610.28694577, 
            "volume_24h": 4021140520.35865, 
            "market_cap": 114348954341.0, 
            "percent_change_1h": -0.21, 
            "percent_change_24h": 0.33, 
            "percent_change_7d": -0.67
        }
    }, 
    "last_updated": 1538381842
}

/* Se define la BD a utilizar */
use cryptongo
/* Se inserta un documento definiendo el nombre de la colección */
db.ticker.insert(documento1)

documento2 = {
    "id": 1, 
    "name": "Bitcoin", 
    "symbol": "BTC", 
    "website_slug": "bitcoin", 
    "rank": 1, 
    "circulating_supply": 17298637.0, 
    "total_supply": 17298637.0, 
    "max_supply": 21000000.0, 
    "quotes": {
        "USD": {
            "price": 6610.28694577, 
            "volume_24h": 4021140520.35865, 
            "market_cap": 114348954341.0, 
            "percent_change_1h": -0.21, 
            "percent_change_24h": 0.33, 
            "percent_change_7d": -0.67
        }
    }, 
    "last_updated": 1538381845
}

/* Se inserta un SOLO documento. Retorna un valor hash como ObjectId */
db.ticker.insertOne(documento2)
/*
    {
        "acknowledged" : true,
        "insertedId" : ObjectId("5bb1da07111da8633812fd37")
    }
*/

documento3 = {
    "id": 2, 
    "name": "Litecoin", 
    "symbol": "LTC", 
    "website_slug": "litecoin", 
    "rank": 7, 
    "circulating_supply": 58531202.0, 
    "total_supply": 58531202.0, 
    "max_supply": 84000000.0, 
    "quotes": {
        "USD": {
            "price": 60.6728675453, 
            "volume_24h": 482685352.468632, 
            "market_cap": 3551255874.0, 
            "percent_change_1h": -0.45, 
            "percent_change_24h": -0.25, 
            "percent_change_7d": 2.91
        }
    }, 
    "last_updated": 1538383082
}

documento4 = {
    "id": 3, 
    "name": "Namecoin", 
    "symbol": "NMC", 
    "website_slug": "namecoin", 
    "rank": 152, 
    "circulating_supply": 14736400.0, 
    "total_supply": 14736400.0, 
    "max_supply": null, 
    "quotes": {
        "USD": {
            "price": 2.097485922, 
            "volume_24h": 76716.7319318829, 
            "market_cap": 30909392.0, 
            "percent_change_1h": 0.43, 
            "percent_change_24h": 18.71, 
            "percent_change_7d": 42.32
        }
    }, 
    "last_updated": 1538383082
}

db.ticker.insertMany([documento3, documento4])
/*
{
    "acknowledged" : true,
    "insertedIds" : [
        ObjectId("5bb1dda6111da8633812fd38"),
        ObjectId("5bb1dda6111da8633812fd39")
    ]
}
*/

/* Trae todos los documentos */
db.ticker.find()
/* Trae las dos primeros documentos */
db.ticker.find().limit(2)
/* Busca un documento que cumpla con un criterio de campos específico */
db.ticker.find({"last_updated": 1538383082})
/* En el shell de mongo muestra el resultado json de una forma más legible */
db.ticker.find({"last_updated": 1538383082}).pretty()
/* Trae el primer documento que cumpla esta condición */
db.ticker.findOne({"last_updated": 1538383082, "total_supply": 14736400})
/* findOne() vendría siendo la unión de las funciones find(), pretty() y limit() */
db.ticker.find({"last_updated": 1538383082, "total_supply": 14736400}).pretty().limit()
/* Trae los documentos en donde coincidan los valores en un campo especifico.
  El $in debe definirse en un array. Aplica si el campo es un dato simple o un array de datos.
*/
db.ticker.find({rank: {$in: [1, 7]}})
/* Trae los documentos que el campo sea mayor al valor indicado */
db.ticker.find({"last_updated": {$gt: 1538381845}})
/* Trae los documentos que el campo sea menor al valor indicado */
db.ticker.find({"last_updated": {$lt: 1538381845}})
/* Trae los documentos que el campo sea mayor o igual al valor indicado */
db.ticker.find({"last_updated": {$gte: 1538381845}})
/* Trae los documentos que el campo sea menor o igual al valor indicado */
db.ticker.find({"last_updated": {$lte: 1538381845}})
/* En la proyecciòn se indica que campos no se desean mostrar en el resultado de la consulta. 1: Si, 0: No */
db.ticker.find({"last_updated": {$gte: 1538381845}}, {"id": 0, "website_slug": 0})

/* Una forma de modificar un documento es guardandolo en una variable, modificar el campo y almacenar el documento nuevamente */
doc_temp = db.ticker.findOne()
doc_temp.website_slug = "bitycoin"
/* La función save() según su _id modifica un documento si ya existe o inserta un documento si no existe. */
db.ticker.save(doc_temp)
db.ticker.save({_id: ObjectId("5bb1d96a111da8633812fd36"), "website_slug": "bitycoin"})
/*
Para update() se debe pasar el query del documento que se desea hacer la modificacion y como proyeccion los campos a modificar.
Nota: Siempre matendra el _id. Si se pasan solo unos campos a modificar, solo colocara estos campos y se eliminara los demas.
  Para estos casos lo mejor es usar save o enviar todo el doccumento ya con el campo modificado previamente.
  Tambien se utiliza enviando todo el documento con campos que se desean eliminar.
*/
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {"website_slug": "bitycoin"})
db.ticker.update({"name": "Bitcoin"}, {"website_slug": "bitycoin"})
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, doc_temp)
/* Modifica (asigna) un valor a un campo especifico. Si no encuentra el campo, lo agrega. */
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {$set: {"website_slug": "bitycoin"}})
/* Elimina un campo especifico de un documento */
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {$unset: {"website_slug": ""}})

doc_original = db.ticker.findOne()
doc_temp = doc_original
doc_temp.quotes.USD.price = 7000  /* Cambia el valor de un subdocumento */
db.ticker.save(doc_temp)
doc_quotes = doc_temp.quotes
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {$unset: {"quotes": ""}})  /* Elimina un subdocumento */
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {$set: {"quotes": doc_quotes}})  /* Añade un subdocumento */

/* Modifica el primer documento que encuente
  Retorna:
    matchedCount: Indica el numero de documentos encontrados.
    modifiedCount: Indica el numero de documentos modificados.
*/
db.ticker.updateOne({"name": "Bitcoin"}, {$set: {"website_slug": "bitcoin"}})
/* Modifica todos los documento que encuente segun el criterio de busqueda. */
db.ticker.updateMany({"name": "Bitcoin"}, {$set: {"website_slug": "bitcoin"}})

/* Incrementa un campo segun el valor especificado */
db.ticker.update({"name": "Bitcoin"}, {$inc: {"rank": 2, "quotes.USD.price": 500}})

db.ticker.find()
/* Inserta un arreglo especificando su nombre. Si no existe, lo crea. Si existe, añade el valor asi ya se encuentre en el arreglo. */
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {$push: {"quotes.scores": 89}})
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {$unset: {"quotes.scores": ""}})
/* Inserta un conjunto de valores aun arreglo especificando su nombre. Si no existe lo crea. Si existe, añade los valores asi ya se encuentre en el arreglo. */
db.ticker.update({_id: ObjectId("5bb3b96df85fb6b9e2a29467")}, {$push: {"quotes.scores": {$each : [90, 91, 92]}}})
/* Agrega un valor a un arreglo. Si ya existe, no lo agrega. */
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {$addToSet: {"quotes.scores": 89 }})
/* Agrega un conjunto de valores a un arreglo. Si ya existen, no los agrega. */
db.ticker.update({_id: ObjectId("5bb1d96a111da8633812fd36")}, {$addToSet: {"quotes.scores": {$each: [89, 90] }}})
/* Con $pop se elimina el primer o ultimo elemento de un array. -1 para eliminar el primer elemento y 1 para eliminar el ultimo elemento. */
db.ticker.update({_id: ObjectId("5bb3b96df85fb6b9e2a29467")}, {$pop: {"quotes.scores": -1}})  // 91, 92
db.ticker.update({_id: ObjectId("5bb3b96df85fb6b9e2a29467")}, {$pop: {"quotes.scores": 1}})  // 91
/* Con $pull se elimina un elemento especifico de un array. Se puede especicar un solo valor o con $in para un conjunto de valores. */
db.ticker.update({_id: ObjectId("5bb3b96df85fb6b9e2a29467")}, {$pull: {"quotes.scores": 90}})
db.ticker.update({_id: ObjectId("5bb3b96df85fb6b9e2a29467")}, {$pull: {"quotes.scores": {$in: [91, 92]}}})


db.ticker.find()
/* Elimina un documento segun un criterio de busqueda. */
db.ticker.remove({_id:ObjectId("5bb27fa7f85fb6b9e2a2945d")})
db.ticker.remove({"name": "Bitcoin"})
/* Elimina una coleccion con todos sus documentos */
db.ticker.drop()