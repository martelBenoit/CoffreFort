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

@app.route('/api/ressource', methods=['GET'])
def verify_token():
        token = request.args.get('token', default = '*', type = str)
        socket.send_json({"validate_token": token})
        message = socket.recv_json()

        if message['valid']:
                return jsonify(pr:"La ressource protégée est ici")
        else:
                return jsonify(pr:"",info="wrong token")


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5200, debug=True)
       