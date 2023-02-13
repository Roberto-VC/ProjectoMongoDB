from flask import request, jsonify, send_file
import pymongo
from bson import json_util
from bson.objectid import ObjectId
import json

# -------- Implementacion de GridFS --------
# Referencias: 
# - https://www.youtube.com/watch?v=d2dp71Vwt0c
# - https://www.youtube.com/watch?v=KSB5g8qt9io
from gridfs import GridFS
import os

def _process_elenco(elencos:str) -> list[dict]:
    elencos = elencos.replace(' ', '')
    elencos = elencos.replace('\n', '')
    elencos = elencos.replace('"', '')
    elencos = elencos[1:-1]
    elencos = elencos.split('},{')

    new_elenco = []
    for actor in elencos:
        temp_elenco:dict = {}
        fields = actor.split(',')

        for field in fields:
            key, value = field.split(':')
            temp_elenco[key] = value

        new_elenco.append(temp_elenco)

    for n in new_elenco:
        n['edad'] = int(n['edad'])
        n['oscar'] = True if n['oscar'] else False

    return new_elenco

def _process_genres(genres:str) -> list[str]:
    genres = genres.replace(' ', '')
    genres = genres.replace('\n', '')
    genres = genres.replace('"', '')
    genres = genres[1:-1]
    genres = genres.split(',')
    return genres

def _process_director(director:str) -> list[str]:
    director = director[1:-1]
    director = director.replace(' ', '')
    director = director.replace('\n', '')
    director = director.replace('"', '')
    director = director.replace("'", '')
    director = director.split(',')

    new_director = {}
    for field in director:
        key, value = field.split(':')
        new_director[key] = value

    return new_director

def createPeli(db, app):
    # ----- Upload de imagen con GridFS
    # revisar que la imagen de portada se envio correctamente
    if 'cover' not in request.files:
        return jsonify({'error': 'file not provided'}), 400
    
    file = request.files['cover']
    if file.filename == '':
        return jsonify({'error': 'no file selected'}), 400
    
    if file.filename.split('.')[1] not in ['png', 'jpeg', 'jpg']:
        return jsonify({'error': 'File not allowed'}), 400
    # guardar archivo temporalmente
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) 
    file.save(temp_path)

    # subir a gridfs
    data = open(temp_path, 'rb').read()
    fs = GridFS(db)
    fs.put(data, filename=file.filename)

    # eliminar archivo temporal
    os.remove(temp_path)

    # Referenciar imagen en movies
    data = db.fs.files.find_one({'filename':file.filename})
    cover_id = data['_id']

    # ----- Crear pelicula
    # transformaciones a elenco
    elencos = _process_elenco(request.form['elenco'])
    
    # transformaciones a genres
    genres = _process_genres(request.form["genres"])
    
    # transformaciones a director
    director = _process_director(request.form["director"])


    # Creacion de pelicula
    db.movies.insert_one({
        "title": request.form['title'],
        "elenco": elencos,
        "director": director,
        "genres": genres,
        "year": int(request.form["year"]),
        "sinopsis": request.form["sinopsis"],
        "duracion": int(request.form["duracion"]),
        "ratings" : [],
        "avg_rating": 0, 
        "comments" : [],
        "cover": cover_id
    })

    return { 'succes': True }

def getPelis(db):
    tuples = []

    for tuple in db.movies.find():
        tuple['_id'] = str(tuple['_id'])
        tuple['cover'] = str(tuple['cover'])
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

def deleteMovie(db):
    try:
        movie_id = ObjectId(request.json['_id'])
        cover_id = db.movies.find_one({ "_id": movie_id })['cover']
        cover_id = ObjectId(cover_id)

        db.movies.delete_one({ "_id": movie_id })
        fs = GridFS(db)
        fs.delete(ObjectId(cover_id))
        return { "succes": True }

    except Exception as e:
        return { 
            "succes": False,
            'error': str(e)
        }

def createUser(db):
    username = request.json["username"]
    id = db.users.insert_one({
        "_id": username,
        "nombre": request.json["nombre"],
        "apellido": request.json["apellido"],
        "password": request.json["password"]
    })
    
    return {"msg": "Recived"}

def getUser(db):
    users = []
    for user in db.users.find({'_id': request.json["username"]}):
        users.append({
            'username': user['_id'],
            'nombre': user['nombre'],
            'apellido': user['apellido'],
            'password': user['password']
        })
    if len(users) == 1:
        temp = users[0]
        if request.json["password"] == temp['password']:
            return {"msg": ":)"}
        else:
            return {"msg": ":|"}
    else:
        return {"msg": ":("}

def deleteUser(db, id):
    db.users.delete_one({'_id': id})
    return jsonify({"msg": 'User deleted'})

def updateUser(db, id):
    db.users.update_one(
        {'_id': ObjectId(id)}, 
        {'$set': {        
        "nombre": request.json["nombre"],
        "apellido": request.json["apellido"],
        "username": request.json["username"],
        "password": request.json["password"]}}
    )
    return jsonify({"msg": 'User Updated'})

def addReview(db, id):
    db.movies.update_one(
        {'_id': ObjectId(id)},
        {'$push': {
            'ratings': request.json["rating"],
            "comments": {"user_id": request.json["username"], "text": request.json["text"]}
        }}
    )
    return jsonify({"msg": "Review Added"})

def findmovie(db, id):
    tuples = []
    for tuple in db.movies.find({'title': {'$regex': id}}):
        tuple['_id'] = str(tuple['_id'])
        tuple['cover'] = str(tuple['cover'])
        tuples.append(tuple)
    return jsonify(tuples)

def findgenre(db, id):
    tuples = []
    for tuple in db.movies.find({'genres': {'$regex': id}}):
        tuple['_id'] = str(tuple['_id'])
        tuple['cover'] = str(tuple['cover'])
        tuples.append(tuple)
    return jsonify(tuples)
    
def getCover(db, id):
    id = ObjectId(id)
    fs = GridFS(db)
    data = fs.get(id)
    print('llego')
    filename = db.fs.files.find_one({'_id': id})['filename']
    return send_file(data, download_name=filename)
