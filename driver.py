# Flask Imports
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

# Controllers
import controllers.peliculasxd as pelis

# App Config
app = Flask(__name__)
app.config['MONGO_URI']="mongodb+srv://peliculas:Mongo123@cluster0.dtfcscy.mongodb.net/pueba?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db.peliculas

# Endpoints
@app.route("/users", methods=["POST"])
def createPeli():
    pelis.createPeli(db)

@app.route("/users", methods=["GET"])
def getPeli():
    return '<h1>recieved'

if __name__ == "__main__":
    app.run(debug = True)