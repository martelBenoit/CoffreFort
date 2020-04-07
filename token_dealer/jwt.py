import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:5555")

if __name__ == "__main__":

	while True:
		# interpreter le message recu, générer un token et le renvoyer ou alors répondre oui ou non si le token recu est valide
		message = socket.recv()
		socket.send(b"Bonjour")