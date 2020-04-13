import time
import zmq
import jwt
import json
from datetime import datetime

if __name__ == "__main__":

	tokens = []
	
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://0.0.0.0:7000")

	print("ouvert")
	while True:
		# interpreter le message recu, générer un token et le renvoyer ou alors répondre oui ou non si le token recu est valide
		message = socket.recv_json()
		if 'login' in message:
	
			encoded_jwt = jwt.encode({'login':message['login'],'datetime':datetime.now().__str__()}, 'secret', algorithm='HS256')
			token = encoded_jwt.decode("utf-8")

			for obj in tokens:
				if obj[0] == message['login']:
					obj[1] = token
				else:
					token.append([message['login'],token])

			socket.send_json({"token":token})

		if 'validate_token' in message:
			try:
				decoded = jwt.decode(message['validate_token'],'secret',algorithm='HS256')
				print(decoded)
				socket.send_json({'valid': True})
			except jwt.exceptions.DecodeError as err:
				socket.send_json({'valid': False})
				
		#if message['token'] is not None:
			#decoded = jwt.decode(message['token'],'secret',algorithm='HS256')


			
		
