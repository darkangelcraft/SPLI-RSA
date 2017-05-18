#from socket import * 
import mysocket
from bitstring import *
from gmpy2 import *
from random import randint
import math
import random 
import sys
import time

filename = 'decrypted.png'
PORT = 55710
CHUNK_DIM=6

'''
def itos(n, length):
    stringa = str(n)
    while (length - len(stringa)) > 0 :
        stringa = '0'+stringa
    return stringa

def myzfill(n, length):
    stringa = str(n)
    while (length - len(stringa)) > 0 :
        stringa = '0'+stringa
    return stringa.encode('ascii')
'''
def myzfill(n, len):
    string=str(n)
    string= string.zfill(len)
    return string.encode('ascii')	
def rabinMiller(n):
     s = n-1
     t = 0
     while s&1 == 0:
         s = s/2
         t +=1
     k = 0
     while k<128:
         a = random.randrange(2,n-1)
         #a^s is computationally infeasible.  we need a more intelligent approach
         #v = (a**s)%n
         #python s core math module can do modular exponentiation
         v = pow(a,s,n) #where values are (num,exp,mod)
         if v != 1:
             i=0
             while v != (n-1):
                 if i == t-1:
                     return False
                 else:
                     i = i+1
                     v = (v**2)%n
         k+=2
     return True

def isPrime(n):
     #lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
     #under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
     #of composite numbers from our potential pool without resorting to Rabin-Miller
     lowPrimes =   [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                   ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                   ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                   ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                   ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                   ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                   ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                   ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                   ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                   ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
     if (n >= 3):
			# n ha come prima cifra 1
         if (n&1 != 0):
             for p in lowPrimes:
                 if (n == p):
                    return True
                 if (n % p == 0):
                     return False
             return rabinMiller(n)
     return False

def generateLargePrime(k):
     #k is the desired bit length
     r=100*(math.log(k,2)+1) #number of attempts max
     r_ = r
     while r>0:
        #randrange is mersenne twister and is completely deterministic
        #unusable for serious crypto purposes
         n = random.randrange(2**(k-1),2**(k))
         r-=1
         if isPrime(n) == True:
             return n
     return "Failure after "+'r_' + " tries."


def eulero(p,q):
	return (p-1)*(q-1)
	
def wait_for_bob():
	#SPLI print("In attesa di Bob")
	ack = mpz((new_sock.receive(6)))	
	
def ack_for_bob():
	#SPLI print("Ack inviato a Bob")
	new_sock.send(myzfill(N,6))	
	
	
	
#####################################################################

#INIZIA NOSTRO PROGRAMMA

#####################################################################

sock = mysocket.mysocket()
sock.bind("localhost", PORT)
sock.listen(5)
print("Server on.")
print("Waiting for connection...")
new_sock, address = sock.accept()
print("Connessione stabilita con: ", address)
new_sock = mysocket.mysocket(new_sock)

#####################################################################
#####################################################################
P = generateLargePrime(6)	#P ha 16 cifre
Q = generateLargePrime(6)	#Q ha 16 cifre
print("Questo e' P: %d " % P)
print("Questo e' Q: %d " % Q)
N = mpz(P*Q)					# N di alice
print("Questo e' N: %d " % N)
fi_eulero = eulero(P,Q)
print("fi e': %d " % fi_eulero)
#calcolo random 1 < e < fi(n)
E = random.randint(2,fi_eulero-1)	
flag= True
while(flag):
	try:
		E = random.randint(2,fi_eulero-1)
		D = invert(E,fi_eulero)
		flag= False
	except:
		vito=True

print("Questo e' E: %d " % E)
print("Questo e' D: %d " % D)

new_sock.send(myzfill(N,6))	#mando N ed E come stringhe da 16 caratteri
new_sock.send(myzfill(E,6))
print("Mando N ed E a Bob")
#SPLI print(N)
#SPLI print(E)

#print("Aspetto ack da Bob")
#ack0 = mpz((new_sock.receive(16)))		

print("Attendo num_chunk da Bob")
chunk_num = int(new_sock.receive(100))	#ricevo num_chunk come stringa da 100 caratteri
print("Num_chunk dell'immagine di Bob: %d" %chunk_num)
#print(chunk_num)
print("Comincio a decifrare!")

#wait bob 1 
#wait_for_bob()

#wait_for_bob()
decifrato = BitStream()
for i in range(chunk_num):
	print str(i)+'/'+str(chunk_num)
	#SPLI print("Entro nel for %d" %i)
	ack_for_bob()
#	new_sock.send(myzfill(N,16))
	chunk = int(new_sock.receive(5000))
	ack_for_bob()
	#SPLI print("Ricevo %d" %chunk)
	de_file = pow(chunk, D, N)	# C^D (mod N)
	if i==0:
		decifrato=BitStream(uint=de_file, length=6)
	else:
		de_file=BitStream(uint=de_file, length=6)		
		decifrato.append(de_file) # da modificare, usare metodo append di BitStream
	#wait bob 2
	wait_for_bob()	#attendo 16 caratteri da Bob
	

time.sleep(4)
decifrato = decifrato.bytes
received_file = open(filename, 'wb')
received_file.write(decifrato)
received_file.close()

print("Operazione completata")
time.sleep(5)
exit()
