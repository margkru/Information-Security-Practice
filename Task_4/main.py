from cryptography.fernet import Fernet

def write_key(): # Создаем ключ и сохраняем его в файл
    key = Fernet.generate_key()
    with open('crypto.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    return open('crypto.key', 'rb').read()

def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open('encrypted.txt', 'wb') as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open('decrypted.txt', 'wb') as file:
        file.write(decrypted_data)


#write_key()  # сгенерировать новый ключ
key = load_key()
encrypt('text.txt', key)  # зашифровать файл
decrypt('encrypted.txt', key)  # расшифровать файл
