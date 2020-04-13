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

        socket.send_json({"validate_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6ImJtYXJ0ZWwiLCJkYXRldGltZSI6IjIwMjAtMDQtMTMgMTI6NTc6MzQuMTA1NjcxIn0.NOkBVFqC4jpf0-PSa4rChjNnXlI-_OGP_PjCl-9wQS0"})
        message = socket.recv_json()
        return jsonify(valid=message['valid'])


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5200, debug=True)
       