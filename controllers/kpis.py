from flask import request, jsonify, send_file
import pymongo
from bson import json_util
from bson.objectid import ObjectId
import json
from gridfs import GridFS
import os

def topActor(db, genre):
    pipeline = [
        { "$unwind": "$genres" },
        { "$unwind": "$elenco" },
        { "$match": { "genres": genre} },
        {
            "$project":
            {
                "genres": 1,
                "elenco": 1
            }
        },
        {
            "$group":
            {
                "_id": {
                    "actor": "$elenco.nombre",
                    "genre": "$genres"
                },
                "count": { "$sum": 1 }
            }
        },
        {
            "$group":
            {
                "_id": "$_id.genre",
                "top_actor": 
                {
                    "$push":
                    {
                        "actor":"$_id.actor",
                        "count": { "$sum": "$count" }
                    }
                }
            }
        },
        { "$unwind": "$top_actor" },
        { "$sort": { "top_actor.count": pymongo.DESCENDING } },
        { "$limit": 1 },
        {
            "$project":
            {
                "actor": "$top_actor.actor"
            }
        }
    ]

    return list(db.movies.aggregate(pipeline))[0]

def topDirector(db, genre):
    pipeline = [
        { '$unwind': "$genres" },
        { '$match': { 'genres': genre} },
        {
            '$project':
            {
                'genres': 1,
                'director': { '$concat': [ "$director.nombre", " ", "$director.apellido"] }
            }
        },
        {
            '$group':
            {
                '_id': {
                    'director': "$director",
                    'genre': "$genres"
                },
                'count': { '$sum': 1 }
            }
        },
        {
            '$group':
            {
                '_id': "$_id.genre",
                'top': 
                {
                    '$push':
                    {
                        'director':"$_id.director",
                        'count': { '$sum' : "$count" }
                    }
                }
            }
        },
        { '$unwind': "$top" },
        { '$sort': { "top.count": -1 } },
        { '$limit': 1 },
        {
            '$project':
            {
                'director': "$top.director"
            }
        }
    ]

    return list(db.movies.aggregate(pipeline))[0]

def topMovies(db):
    pipeline = [
        {
            "$project":
            {
                "title": 1,
                "avg_rating": { "$sum": "$ratings" }
            }
        },
        { "$sort": {"avg_rating": pymongo.DESCENDING} },
        { "$limit": 3}
    ]
    movies = list(db.movies.aggregate(pipeline))
    for m in movies:
        m['_id'] = ''

    return movies