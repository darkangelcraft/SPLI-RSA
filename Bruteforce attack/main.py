import math
from bitstring import *
from gmpy2 import *
import time
from random import randint
import struct
# from socket import *
import mysocket
import random


# import socket

####################################################
#	
# FUNZIONI
#
####################################################
def myzfill(n, len):
    string = str(n)
    string = string.zfill(len)
    return string.encode('ascii')

def rabinMiller(n):
    s = n - 1
    t = 0
    while s & 1 == 0:
        s = s / 2
        t += 1
    k = 0
    while k < 128:
        a = random.randrange(2, n - 1)
        # a^s is computationally infeasible.  we need a more intelligent approach
        # v = (a**s)%n
        # python s core math module can do modular exponentiation
        v = pow(a, s, n)  # where values are (num,exp,mod)
        if v != 1:
            i = 0
            while v != (n - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % n
        k += 2
    return True


def isPrime(n):
    # lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
    # under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
    # of composite numbers from our potential pool without resorting to Rabin-Miller
    lowPrimes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
        , 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179
        , 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269
        , 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367
        , 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461
        , 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571
        , 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661
        , 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773
        , 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883
        , 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    if (n >= 3):
        if (n & 1 != 0):
            for p in lowPrimes:
                if (n == p):
                    return True
                if (n % p == 0):
                    return False
            return rabinMiller(n)
    return False


def generateLargePrime(k):
    # k is the desired bit length
    r = 100 * (math.log(k, 2) + 1)  # number of attempts max
    r_ = r
    while r > 0:
        # randrange is mersenne twister and is completely deterministic
        # unusable for serious crypto purposes
        n = random.randrange(2 ** (k - 1), 2 ** (k))
        r -= 1
        if isPrime(n) == True:
            return n
    return "Failure after " + 'r_' + " tries."


def eulero(p, q):
    return (p - 1) * (q - 1)


def factor(n):
    if (n % 2 == 0):
        return 2
    i = 3
    while True:
        # print("Numero sotto test %i" %i)
        if (n % i == 0):
            return i
        else:
            i = i + 2


def wait_for_bob():
    print("In attesa di Bob")
    ack = mpz((sock.receive(8)))


def ack_for_bob():
    print("Ack inviato a Bob")
    sock.send(myzfill(N, 8))


####################################################
#	
# INIZIO PROGRAMMA
#
####################################################

# Preparativi
# PARTE DI CONNESSIONE VERSO BOB
filename = 'decrypted.jpg'
BOB = "localhost"  # INDIRIZZO DI BOB
PORT = 55711
CHUNK_DIM = 14

t1=time.time()
# Bob sta aspettando mi connetta a lui
sock = mysocket.mysocket()
print("Inizio la connessione:")
sock.connect(BOB, PORT)
print("Connesso a %s:%d" % (BOB, PORT))

# Attendo N ed E
print("Attendo N, E, num_chunk")
N = mpz((sock.receive(8)))  # ricevo N
print("Ho ricevuto N %d" % N)
E = mpz((sock.receive(8)))  # ricevo E
print("Ho ricevuto E %d" % E)

# ack 1 per bob
ack_for_bob()

print("Attendo chunk_num")
chunk_num = int(sock.receive(100))
print("Ho ricevuto chunk_num %d" % chunk_num)

# Attacco
print("Inizio tentativo di rottura RSA")
# Calolo D
P = factor(N)
P = mpz(P)
print("Ho trovato P, e' %d" % P)
# Q = N/P
Q = mpz(N / P)
print("Q e'%d" % Q)
fi_eulero = eulero(P, Q)
print("fi e'%d" % fi_eulero)
flag = True
while (flag):
    try:
        D = invert(E, fi_eulero)
        flag = False
    except:
        vito = True
print("Questo e' D: %d " % D)


##############################
f=open("log.txt", 'ab')
f.write("D--->"+str(D)+"    N--->"+str(N)+"\n")
f.close()

##############################
t2=time.time()
# ack 2 per bob
ack_for_bob()

# wait ack 1 per bob
# wait_for_bob()

# wait_for_bob()
print("Comincio a decifrare!")

# Decifratura
decifrato = BitStream()
print("Num_chunk e' %d" % chunk_num)
for i in range(chunk_num):
    print("Entro nel for %d" % i)
    ack_for_bob()
    chunk = int(sock.receive(5000))
    ack_for_bob()
    print("Ricevo %d" % chunk)
    print "\n"
    de_file = pow(chunk, D, N)
    print ("DE_file:: %d"%de_file)
    if i == 0:
        decifrato = BitStream(uint=de_file, length=CHUNK_DIM)
    else:
        de_file = BitStream(uint=de_file, length=CHUNK_DIM)
        decifrato.append(de_file)  # da modificare, usare metodo append di BitStream
    wait_for_bob()

#scrittura su file del contenuto decriptato
try:
    f=open(filename, 'wb')
    BitStream(decifrato).tofile(f)
    f.close()
except IOError:
    print("Cannot save the decrypted file\n'")
    sys.exit(-3)

t3=time.time()
print("Operazione completata\n Tempo impiegato per trovare D %.7f "%(t2-t1)+" sec.")
print("Tempo impiegato (totale) %.7f "%(t3-t1)+" sec.")
'''
decifrato = decifrato.bytes
received_file = open(filename, 'wb')
received_file.write(decifrato)
received_file.close()
'''

print("\033[93mOperazione completata\033[0m")
