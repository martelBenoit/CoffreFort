import os
import json
from flask import(Flask, jsonify, request, g)
import flasgger
import zmq

app = Flask(__name__)
swagger = flasgger.Swagger(app)

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://tokendealer:7000")

@app.route('/api', methods=['GET'])
def new_user():
        return jsonify(hello='world')


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5200, debug=True)
       