import time
import zmq
import jwt
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
		if message['login'] is not None:
			
			encoded_jwt = jwt.encode({'login': message['login'],'datetime':datetime.now()}, 'secret', algorithm='HS256')
			token = encoded_jwt.decode("utf-8")

			for obj in tokens:
				if obj[0] == message['login']:
					obj[1] = token
				else:
					token.append([message['login'],token])

			socket.send_json({"token":token})

		#if message['token'] is not None:
			#decoded = jwt.decode(message['token'],'secret',algorithm='HS256')


			
		
