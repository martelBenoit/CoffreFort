import os
import json
import hashlib
from flask import(Flask, jsonify, request, g)
import pymongo
from jsonschema import validate
import flasgger
import zmq

app = Flask(__name__)
swagger = flasgger.Swagger(app)

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://tokendealer:5555")

with open("./userSchem.json", "r") as f:
        schem = json.load(f)

client = pymongo.MongoClient('mongodb://root:root@mongodb:27017')
db = client.usersdb
users = db["users"]
users.create_index([('login',pymongo.ASCENDING)],unique=True)

@app.before_request
def authenticate():
        if request.authorization:
                g.user = request.authorization['username']
                g.password = request.authorization['password']
        else:
                g.user = 'Anonymous'

@app.route('/')
def index():
        info = "Welcome "+g.user
        return jsonify(
                message=info
                )

@app.route('/api/users', methods=['POST'])
@flasgger.swag_from('docs/registration_user.yml')
def new_user():
        content = request.get_json()
        if verify_scheme(content):
                user = {'login':content['LOGIN'],
                'password':hashPassword(content['PASSWORD']),
                }
                try:
                        users.insert_one(user).inserted_id
                except pymongo.errors.DuplicateKeyError as dke:
                        reason = content['LOGIN']+" is already used"
                        return jsonify(registration=False,reason=reason)
                except Exception as ex:
                        return jsonify(registration=False,reason="Database error")
                else:
                        return jsonify(registration=True)
        else:
                return jsonify(registration=False,reason="Invalid parameters")


@app.route('/api/users/<login>', methods=['PUT'])
@flasgger.swag_from('docs/change_password.yml')
def change_password(login):
        if(g.user == login):
                user = users.find_one({"login":login})
                if user != None:
                        if verifyPassword(g.password,user['password']):
                                content = request.get_json()
                                password = content['PASSWORD']
                                if len(password) < 6:
                                        return jsonify(update=False,reason="Password length too short")
                                if password != None:
                                        try:
                                                users.update({"login":login},{"login":login,"password":hashPassword(password)})
                                        except Exception as ex:
                                                return jsonify(update=False,reason=ex)
                                        else:
                                                return jsonify(update=True,reason="")
                                else:
                                        return jsonify(update=False,reason="Invalid parameter password")
                        else:
                                return jsonify(update=False,reason="Incorrect password")
                else:
                        return jsonify(update=False,reason="Incorrect login")
        else:
                return jsonify(update=False,reason="Permission denied")

@app.route('/api/users/<login>', methods=['DELETE'])
def delete(login):
        if(g.user == login):
                user = users.find_one({"login":login})
                if user != None:
                        if verifyPassword(g.password,user['password']):
                                users.delete_one({"login":login})
                                return jsonify(deleted=True)
                        else:
                                return jsonify(deleted=False,reason="Incorrect password")
                else:
                        return jsonify(deleted=False,reason="Incorrect login")
        else:
                return jsonify(deleted=False,reason="Permission denied")


@app.route('/api/users/<login>', methods=['GET'])
def info(login):
        if(g.user == login):
                user = users.find_one({"login":login})
                if user != None:
                        if verifyPassword(g.password,user['password']):
                                return jsonify(login=user['login'])
                        else:
                                return jsonify()
                else:
                        return jsonify()
        else:
                return jsonify()

@app.route('/api/auth', methods=['GET'])
def auth():

        user = users.find_one({"login":g.user})
        if user != None:
                if verifyPassword(g.password,user['password']):
                        return jsonify(auth=True)
                else:
                        return jsonify(auth=False,reason="Incorrect password")
        else:
                return jsonify(auth=False,reason="Permission denied")

@app.route('/api/token', methods=['GET'])
def get_token():

        user = users.find_one({"login":g.user})
        if user != None:
                if verifyPassword(g.password,user['password']):
                        # appeler le serveur qui génère un token
                        socket.send(b'Hello')
                        message = (socket.recv()).decode('utf-8')
                        return jsonify(token=message)
                else:
                        return jsonify(token="",reason="Incorrect password")
        else:
                return jsonify(token="",reason="Permission denied")
        

def verify_scheme(test):
        try:
                validate(test,schem)
        except Exception as valid_err:
                print("Validation KO: {}".format(valid_err))
                return False
        else:
                return True

def hashPassword(password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000)
        return salt+key

def verifyPassword(password, hash):
        salt = hash[:32]
        keyPassword = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000)
        keyHash = hash[32:]
        if keyPassword == keyHash:
                return True
        else:
                return False

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
        with open("./testValidUser.json", "r") as f:
                jsonTest = json.load(f)
        