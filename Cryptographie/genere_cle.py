from cryptography.fernet import Fernet


cle = Fernet.generate_key()
file = open("cle_chiffrement.txt", 'wb')
file.write(cle)
file.close()

