from flask import request

def createPeli(db):
    id = db.insert_one({
        "_id": request.json["_id"],
        "Nombre-de-la-pelicula": request.json["Nombre-de-la-pelicula"],
        "Año-de-la-pelicula": request.json["Año-de-la-pelicula"],
        "Genero-de-la-pelicula": request.json["Genero-de-la-pelicula"],
        "Precio-de-la-entrada-de-la-pelicula": request.json["Precio-de-la-entrada-de-la-pelicula"],
    })
    return 'recieved'