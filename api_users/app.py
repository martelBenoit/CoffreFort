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

# Artifacts used to connect to the tokendealer service
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://tokendealer:7000")

# Chargement du schéma de validation du json
with open("./userSchem.json", "r") as f:
        schem = json.load(f)

# Connection à la base de donnée
client = pymongo.MongoClient('mongodb://root:root@mongodb:27017')
db = client.usersdb
# Récupération de la collection users si elle existe sinon création
users = db["users"]
# Création d'un index sur le champs login permettant au login d'être unique
users.create_index([('login',pymongo.ASCENDING)],unique=True)

@app.before_request
def authenticate():
        if request.authorization:
                g.user = request.authorization['username']
                g.password = request.authorization['password']
        else:
                g.user = 'Anonymous'

@app.route('/api/users', methods=['POST'])
@flasgger.swag_from('docs/registration_user.yml')
def new_user():
        content = request.get_json()
        print(content)
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
@flasgger.swag_from('docs/delete_user.yml')
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
@flasgger.swag_from('docs/info_user.yml')
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

# Recepteur de l'API utilise lors de la connexion depuis la page d'accueil
# Fait office d'authentification et de generation de token
@app.route('/api/token', methods=['GET'])
@flasgger.swag_from('docs/get_token.yml')
def get_token():

        user = users.find_one({"login":g.user})
        if user != None:
                if verifyPassword(g.password,user['password']):
                        try:
                                socket.send_json({"login": g.user})
                                message = socket.recv_json()
                                return jsonify(token=message['token'])
                        except Exception as err:
                                return jsonify(token="",reason="unable to contact the token server")
                        
                else:
                        return jsonify(token="",reason="Incorrect password")
        else:
                return jsonify(token="",reason="Permission denied")
           
@app.route('/api/logout', methods=['POST'])
@flasgger.swag_from('docs/logout.yml')
def logout():
        content = request.get_json()
        user = users.find_one({"login":content["LOGIN"]})
        if users != None :
                socket.send_json({"logout": content["TOKEN"]})
                message = socket.recv_json()
                return jsonify(logout=message['logout'])
        else:
                return jsonify(logout=False,reason="Unknown user")

# Permet de vérifier le schéma json d'inscription
def verify_scheme(test):
        try:
                validate(test,schem)
        except Exception as valid_err:
                print("Validation KO: {}".format(valid_err))
                return False
        else:
                return True

# Permet d'hasher le mot de passe passé en paramètre
def hashPassword(password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000)
        return salt+key

# On vérifie si le mot de passe est correcte
def verifyPassword(password, hash):
        # Récupération du sel du mot de passe hashé en bdd 
        salt = hash[:32]
        # Hash du mot de passe passé en paramètre en utilisant le hash du mot de passe en bdd  
        keyPassword = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000)
        # Récupération du hash du mot de passe en bdd 
        keyHash = hash[32:]
        # Comparaison des deux hashs 
        if keyPassword == keyHash:
                return True
        else:
                return False

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)