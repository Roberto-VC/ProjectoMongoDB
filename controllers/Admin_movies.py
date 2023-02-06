from flask import request, jsonify
import pymongo
from bson.objectid import ObjectId

def createPeli(db):
    elencos = request.json['elenco']

    for n in elencos:
        n['edad'] = int(n['edad'])
        n['oscar'] = True if n['oscar'] else False
    
    id = db.movies.insert_one({
        "title": request.json['title'],
        "elenco": elencos,
        "director": request.json['director'],
        "genres": request.json["genres"],
        "year": int(request.json["year"]),
        "sinopsis": request.json["sinopsis"],
        "duracion": int(request.json["duracion"]),
        "ratings" : [],
        "avg_rating": 0, 
        "comments" : []
    })

    return { 
        "succes": True,
        "new_id": str(id)
    }

def getPelis(db):
    tuples = []

    for tuple in db.movies.find():
        tuple['_id'] = str(tuple['_id'])
        tuples.append(tuple)

    return jsonify(tuples)

def addActor(db):
    try:
        new_elenco = request.json['elenco']
        new_elenco['edad'] = int(new_elenco['edad'])
        new_elenco['oscar'] = True if new_elenco['oscar'] else False

        db.movies.update_one(
            { "_id": ObjectId(request.json['_id']) },
            { "$addToSet": { "elenco": new_elenco } }
        )

        return { "succes": True }

    except:
        return { "succes": False }

def addGenre(db):
    try:
        db.movies.update_one(
            { "_id": ObjectId(request.json['_id']) },
            { "$addToSet": { "genres": request.json['genre'] } }
        )
        return { "succes": True }

    except:
        return { "succes": False }

def editMovie(db):
    try:
        new_value = request.json['new']
        try:
            new_value = int(new_value)
        except:
            pass

        db.movies.update_one(
            { "_id": ObjectId(request.json['_id']) },
            { "$set": { request.json['field']: new_value } }
        )
        return { "succes": True }

    except:
        return { "succes": False }

