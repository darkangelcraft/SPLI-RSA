import sys
from bitstring import *
from gmpy2 import *
from random import randint
import struct
#from socket import *
import mysocket
#import socket
####################################################
#	
#FUNZIONI
#
####################################################

def itos(n, length):
    stringa = str(n)
    while (length - len(stringa)) > 0 :
        stringa = '0'+stringa
    return stringa

def itob(n, length):
    stringa = itos(n, length)
    return stringa.encode('ascii')


def wait_for_oracle():
	print "In attesa di Oracle"
	ack = mpz((new_sockoracle.receive(6)))	
	
def ack_for_oracle():
	print "Ack inviato ad Oracle"
	new_sockoracle.send(itob(N,6))	
	
def wait_for_alice():
	#SPLI print("In attesa di Alice")
	ack = mpz((sock.receive(6)))	
	
def ack_for_alice():
	#SPLI print("Ack inviato ad Alice")
	sock.send(itob(N,6))	
	

####################################################
#	
#INIZIO PROGRAMMA
#
####################################################

ALICE = "192.168.56.101"
PORT = 55710
CHUNK_DIM = 6

#Apro L'immagine da dovere cifrare
try:
	image = BitStream(filename = './zane.jpg')
except IOError:
	print 'Immagine non trovata.'
	sys.exit(0)

image_len = image.length
print "Immagine caricata: %d Bits" % image_len

#FACCIO UN PADDING
resto = image_len % CHUNK_DIM	# verifico che il numero di bits dell'immagine sia multiplo esatto di CHUNK_DIM=16
if (resto != 0 ):
	for i in range(CHUNK_DIM - resto):
		image.append('0b0')
	image_len = image.length
	print 'L\'immagine e\' stata modificata.'
	print "Immagine : %d Bits" % image_len
	
#controllo di quanti chunk e' formata l'immagine
num_chunk = image_len/CHUNK_DIM
print 'La nostra immagine e\' composta da: %d chunk, ciascuno di 6 bits' % num_chunk

'''
#Aspetto Oracle
sockoracle = mysocket.mysocket()
#SPLI sockoracle.bind("0.0.0.0", PORT)
sockoracle.bind("localhost", PORT)
sockoracle.listen(5)
print("Server on.")
print("Waiting for connection...")
new_sockoracle, address2 = sockoracle.accept()
print("Connessione stabilita con: ", address2)
new_sockoracle = mysocket.mysocket(new_sockoracle)
'''

#Mi collego ad Alice
sock = mysocket.mysocket()
print "Inizio la connessione:"
#SPLI sock.connect(ALICE, PORT)
sock.connect("localhost", PORT)
print "Connesso ad Alice, PORT %d" % PORT

# (mpz() serve per gestire numeri grandi in python)
N = mpz((sock.receive(6)))	# ricevo N da 16 caratteri
E = mpz((sock.receive(6)))	# ricevo E da 16 caratteri

print "Ho ricevuto N da Alice: %d" % N
print "Ho ricevuto E da Alice: %d" % E

#####################################################
#####################################################
#li invio a Oracle!
'''
new_sockoracle.send(itob(N,16))
print("Ho inviato N ad Orwell %d" % N)
new_sockoracle.send(itob(E,16))
print("Ho inviato E ad Orwell %d" % E)

#Attesa 1 per Oracle
wait_for_oracle()
'''
####################################################
####################################################

#mando il numero di chunk che compone l' immagine a Alice 
print "Ho inviato num_chunk ad Alice %d" % num_chunk
sock.send(itob(num_chunk,100)) 

'''
#l invio anche ad oracle!
print("Ho inviato num_chunk ad Orwell %d" % num_chunk)
new_sockoracle.send(itob(num_chunk,100)) 
'''
'''
#Attesa 2 per Oracle
print("Alice mi aspetta")
wait_for_oracle()
'''
#Ack 1 per Alice


#SPLI print("Num_chunk e' %d" %num_chunk)	
for i in range(num_chunk):
	#ack_for_alice()
	#ack_for_oracle()
	#SPLI print("Ciclo %d" %i)
	chunk = BitStream(bin = image.read('bin:6'))	#leggo 16 caratteri dell'immagine
	chunk_to_int =chunk.uint	#converto in uint i 16 caratteri dell'immagine appena letti
	###################
	if chunk_to_int >= N:
		print "ERROR: chunk_to_int >= N "
		exit()
	en_file = pow(chunk_to_int, E, N)	#M^e (mod N)
	wait_for_alice()	#attendo un ack da Alice di 16 caratteri
	#SPLI print("Mando ad Alice: %d" %en_file)
	sock.send(itob(en_file,5000))	#trasmetto 5000 caratteri
	wait_for_alice()	#attendo la conferma di Alice
	
	#SPLI	wait_for_oracle()
	#SPLI	print("Mando ad Oracle: %d" %en_file)
	#SPLI	new_sockoracle.send(itob(en_file,5000))
	#SPLI	wait_for_oracle()
	#SPLI	ack_for_oracle()
	
	ack_for_alice()	# trasmetto l'ack di 16 caratteri ad Alice 
	#SPLI	ack_for_oracle()

print "Operazione completata"
exit()
