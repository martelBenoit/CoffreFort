import time
import zmq
import jwt
import json
from datetime import datetime
from datetime import timedelta  

if __name__ == "__main__":

	tokens = []
	
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://0.0.0.0:7000")

	print("ouvert")
	while True:
		# interpreter le message recu, generer un token et le renvoyer ou alors répondre oui ou non si le token recu est valide
		message = socket.recv_json()

		# Generation et stockage du token
		if 'login' in message:
	
			encoded_jwt = jwt.encode({'login':message['login'],'datetime':datetime.now().__str__()}, 'secret', algorithm='HS256')
			token = encoded_jwt.decode("utf-8")

			found = False
			for obj in tokens:
				if obj[0] == message['login']:
					obj[1] = token
					found = True
			
			if not found:
				tokens.append([message['login'],token])

			socket.send_json({"token":token})

		# Verification de la validite du token
		if 'validate_token' in message:
				
			try:
				decoded = jwt.decode(message['validate_token'],'secret',algorithm='HS256')
			
				if [decoded['login'],message['validate_token']] in tokens:
					datetime_object = datetime.strptime(decoded['datetime'], '%Y-%m-%d %H:%M:%S.%f')
					if datetime.now() - datetime_object <= timedelta(hours = 1):
						socket.send_json({'valid': True})
					else:
						socket.send_json({'valid': False})
				else:
					socket.send_json({'valid': False})

			except jwt.exceptions.DecodeError as err:
				socket.send_json({'valid': False})
		
		# Effacement du token pour la deconnexion
		if 'logout' in message:
			try:
				decoded = jwt.decode(message['logout'],'secret',algorithm='HS256')
			
				if [decoded['login'],message['logout']] in tokens:
					datetime_object = datetime.strptime(decoded['datetime'], '%Y-%m-%d %H:%M:%S.%f')
					if datetime.now() - datetime_object <= timedelta(hours = 1):
						tokens.remove([decoded['login'],message['logout']])
						socket.send_json({'logout': True})
					else:
						tokens.remove([decoded['login'],message['logout']])
						socket.send_json({'logout': True})
				else:
					socket.send_json({'logout': False})

			except jwt.exceptions.DecodeError as err:
				socket.send_json({'logout': False})