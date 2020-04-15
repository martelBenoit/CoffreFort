import os
import json
from flask import(Flask, jsonify, request, g)
import flasgger
import zmq

app = Flask(__name__)
swagger = flasgger.Swagger(app)

# connexion serveur zmq (service tokendealer port 7000)
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://tokendealer:7000")

# une seule route GET permettant d'accéder à la ressource 
@app.route('/api/ressource', methods=['GET'])
def verify_token():
		# on récupère le token depuis le paramètre token de notre requête
        token = request.args.get('token', default = '*', type = str)
        # envoi au tokendealer du token pour validation
        socket.send_json({"validate_token": token})
        # réception de la réponse du token dealer
        message = socket.recv_json()

        # si le message de retour indique que le token est valide alors on retourne la ressource protégée
        if message['valid']:
                return jsonify(pr="La ressource protégée est ici")
        # sinon on envoi pas la ressource et on dit pourquoi
        else:
                return jsonify(pr="",info="wrong token")

# le serveur se lance et tourne sur localhost:5200
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5200, debug=True)
       