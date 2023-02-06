# Flask Imports
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

# Controllers
import controllers.Admin_movies as admin

# App Config
app = Flask(__name__)
app.config['MONGO_URI']="mongodb+srv://peliculas:Mongo123@cluster0.dtfcscy.mongodb.net/Proyecto1?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

# -------------- Endpoints --------------

# Admin movies CRUD
@app.route("/createMovie", methods=["POST"])
def createPeli():
    return admin.createPeli(db)

@app.route("/getMovies", methods=["GET"])
def getPeli():
    return admin.getPelis(db)

@app.route("/addActor", methods=["POST"])
def addActor():
    return admin.addActor(db)

@app.route("/addGenre", methods=["POST"])
def addGenre():
    return admin.addGenre(db)

@app.route("/editMovie", methods=["POST"])
def editMovie():
    return admin.editMovie(db)

# -------------- Run API --------------
if __name__ == "__main__":
    app.run(debug = True)
