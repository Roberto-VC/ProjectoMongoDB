
# app.py
from flask import Flask, request, jsonify
import controllers.peliculasxd as pelis


countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

def _find_next_id():
    return max(country["id"] for country in countries) + 1


# -------- APP ---------
app = Flask(__name__)
@app.route('/')
def home():
	return ''

def run():
    app.run(
		host='0.0.0.0',
		port=8000
    )
    print('API Running in port 8000')

@app.get("/peliculas")
def get_peliculas():
    return pelis.get_peliculas()

# Este es un ejemplo que encontre jejej
@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

run()