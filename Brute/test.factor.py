n = 100123
flag = True
i = 2
if(n%2 == 0):
	i=2
	flag=False
	i = i - 1
i = i + 1
while flag:
	print("Numero sotto test %i" %i)
	if (n%i == 0):
		flag=False
	else:
		i = i + 2
print("i %d" %i)