import time
import zmq
import jwt


if __name__ == "__main__":
	
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://0.0.0.0:7000")

	print("ouvert")
	while True:
		# interpreter le message recu, générer un token et le renvoyer ou alors répondre oui ou non si le token recu est valide
		message = socket.recv_json()
		socket.send(b"Bonjour")
		print(message)
