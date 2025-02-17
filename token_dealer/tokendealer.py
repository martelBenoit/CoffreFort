import time
import zmq
import jwt
import json
import random
import string
from datetime import datetime
from datetime import timedelta  

def randomKey():
	randomSource = string.ascii_letters + string.digits + string.punctuation
	key = random.choice(string.ascii_lowercase)
	key += random.choice(string.ascii_uppercase)
	key += random.choice(string.digits)
	key += random.choice(string.punctuation)

	for i in range(6):
		key += random.choice(randomSource)

	keyList = list(key)
	random.SystemRandom().shuffle(keyList)
	key = ''.join(keyList)
	return key

if __name__ == "__main__":

	# on génére un string random pour la clé
	key = randomKey()

	# liste des tokens générés
	tokens = []
	
	# démarrage du serveur zmq
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://0.0.0.0:7000")

	# tant que le programme tourne
	while True:
		# on recoit un message 
		message = socket.recv_json()
		# si le message contient la clé 'login' -> on tente de générer un nouveau token
		if 'login' in message:
			# on génère un token avec comme valeur le login de l'utilisateur, et la date de création
			encoded_jwt = jwt.encode({'login':message['login'],'datetime':datetime.now().__str__()}, key, algorithm='HS256')

			# on passe le token en utf8
			token = encoded_jwt.decode("utf-8")

			# on vient itérer sur notre liste de token pour vérifier si cet utilisateur n'a pas déjà un token actif,
			# si oui alors on remplace le token actuel par le nouveau qui vient d'être généré
			found = False
			for obj in tokens:
				if obj[0] == message['login']:
					obj[1] = token
					found = True

			# sinon on ajoute l'utilisateur accompagné de son token dans la liste des tokens
			if not found:
				tokens.append([message['login'],token])

			# on répond en renvoyant le token généré
			socket.send_json({"token":token})

		# si le message contient la clé 'validate_token' -> on tente de tester si le token est correcte
		if 'validate_token' in message:
				
			try:
				# on décode le token
				decoded = jwt.decode(message['validate_token'],key,algorithm='HS256')
				
				# on regarde si le token se trouve dans notre lisete de token
				if [decoded['login'],message['validate_token']] in tokens:
					# si oui on récupère la date et on regarde si le token est pas plus vieux qu'une heure
					datetime_object = datetime.strptime(decoded['datetime'], '%Y-%m-%d %H:%M:%S.%f')
					if datetime.now() - datetime_object <= timedelta(hours = 1):
						# si oui alors on dit que le token est valide sinon non
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
				decoded = jwt.decode(message['logout'],key,algorithm='HS256')
			
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