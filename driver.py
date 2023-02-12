# Flask Imports
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

# Controllers
import controllers.movies_CRUD as mcrud

# App Config
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = './controllers/temp'
app.config['MONGO_URI']="mongodb+srv://peliculas:Mongo123@cluster0.dtfcscy.mongodb.net/Proyecto1?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

# -------------- Endpoints --------------

# Admin movies CRUD
@app.route("/createMovie", methods=["POST"])
def createPeli(): 
    return mcrud.createPeli(db, app)

@app.route("/getMovies", methods=["GET"])
def getPeli():
    return mcrud.getPelis(db)

@app.route("/addActor", methods=["POST"])
def addActor():
    return mcrud.addActor(db)

@app.route("/addGenre", methods=["POST"])
def addGenre():
    return mcrud.addGenre(db)

@app.route("/editMovie", methods=["POST"])
def editMovie():
    return mcrud.editMovie(db)

@app.route("/addCover", methods=["POST"])
def addCover():
    return mcrud.addCover(db, app)

@app.route("/deleteMovie", methods=["POST"])
def deleteMovie():
    return mcrud.deleteMovie(db)

@app.route("/signup", methods=["POST"])
def createUser():
    return mcrud.createUser(db)

@app.route("/login", methods=["POST"])
def getUser():
    return mcrud.getUser(db)

@app.route("/signup/<id>", methods=["DELETE"])
def deleteUser(id):
    return mcrud.deleteUser(db,id)


@app.route("/signup/<id>", methods=["PUT"])
def updateUser(id):
    return mcrud.updateUser(db,id)

@app.route("/review/<id>", methods=["PUT"])
def addReview(id):
    return mcrud.addReview(db,id)

# -------------- Run API --------------
if __name__ == "__main__":
    app.run(debug = True)
