import os

print 'choose length chunk:'
print '1)  6 bit'
print '2) 64 bit'

choose = raw_input()
if choose == "1":
    os.chdir("RSA(6)")
    print '1) Alice'
    print '2) Bob'

    option=raw_input()
    if option == "1":
        os.chdir("Alice")
        os.system('python mainAlice.py')

    elif option == "2":
        os.chdir("Bob")
        os.system('python mainBob.py')

elif choose == "2":
    os.chdir("RSA(64)")
    print '1) Alice'
    print '2) Bob'

    option = raw_input()
    if option == "1":
        os.chdir("Alice")
        os.system('python mainAlice.py')

    elif option == "2":
        os.chdir("Bob")
        os.system('python mainBob.py')

