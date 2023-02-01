from .conn import db

def get_peliculas():
    peliculas = []
    for movie in db.peliculas.find():
        peliculas.append(movie)
    return peliculas