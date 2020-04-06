import os
from flask import(Flask, jsonify, request)
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client.tododb

@app.route('/')
def index():
        return jsonify(
                status=True,
                message='Welcome !'
                )

@app.route('/api', methods=['POST','DELETE','GET'])
def home():
        print(request)
        print(request.environ)
        response = jsonify({'Hello':'World'})
        print(response)
        print(response.data)
        return response

@app.route('/api/person/<int:person_id>')
def person(person_id):
        response = jsonify({'Hello':person_id})
        return response

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

