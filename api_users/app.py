import os
import json
import hashlib
from flask import(Flask, jsonify, request, g)
import pymongo
from jsonschema import validate


app = Flask(__name__)

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
                print(request.authorization['password'])
        else:
                g.user = 'Anonymous'

@app.route('/')
def index():
        info = "Welcome "+g.user
        return jsonify(
                message=info
                )

@app.route('/api/users', methods=['POST'])
def new_user():
        print(request.is_json)
        content = request.get_json()
        if verify_scheme(content):
                user = {'login':content['LOGIN'],
                'password':hashPassword(content['PASSWORD']),
                }
                try:
                        users.insert_one(user).inserted_id
                except pymongo.errors.DuplicateKeyError as dke:
                        reason = content['LOGIN']+" is already used"
                        return jsonify(registration="ko",reason=reason)
                except Exception as ex:
                        return jsonify(registration="ko",reason="Database error")
                else:
                        return jsonify(registration="ok")
        else:
                return jsonify(registration="ko",reason="")


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
        


