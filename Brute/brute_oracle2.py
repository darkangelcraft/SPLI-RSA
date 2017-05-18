
decifrato = BitStream()
for i in range(chunk_num):
	chunk = int(sock.receive(5000))
	de_file = pow(chunk, D, N)
	if i==0:
		decifrato=BitStream(uint=de_file, length=6)
	else:
		de_file=BitStream(uint=de_file, length=6)		
		decifrato.append(de_file) # da modificare, usare metodo append di BitStream
decifrato = decifrato.bytes
received_file = open(filename, 'wb')
received_file.write(decifrato)
received_file.close()



