import time
import zmq
import jwt


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
			print (message['login'])
			encoded_jwt = jwt.encode({'login': message['login']}, 'secret', algorithm='HS256')
			token = encoded_jwt.decode("utf-8")
			tokens.append({message['login'],token})
			print(token)
			socket.send_json({"token":token})
		else:
			socket.send_json({"token":""})
		
