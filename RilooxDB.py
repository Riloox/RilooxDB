#riloox 15/3/25

import json
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

class RilooxDB:
    def __init__(self, filename="rilooxdb.json", key_file="secret.key"):
        self.filename = filename
        self.key_file = key_file
        try:
            with open(key_file, "rb") as kf:
                key = kf.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(key_file, "wb") as kf:
                kf.write(key)
        self.cipher = Fernet(key)
        self.store = {}
        self.load()

        
    def load(self):
        try:
            with open(self.filename, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            self.store = json.loads(decrypted_data.decode('utf-8'))
        except (FileNotFoundError, ValueError, InvalidToken):
            self.store = {}
    
    def save(self):
        json_data = json.dumps(self.store).encode('utf-8')
        encrypted_data = self.cipher.encrypt(json_data)
        with open(self.filename, 'wb') as f:
            f.write(encrypted_data)

    def create(self, key, value):
        self.store[key] = value
        self.save()
        return f"Guardado {key} con valor {value}"
        
    
    def read(self, key):
        return self.store.get(key, "Llave no encontrada")
    
    def update(self, key, value):
        if key in self.store:
            self.store[key] = value
            self.save()
            return f"Actualizado {key} a valor {value}"
        return "Key not found"
    
    def delete(self, key):
        if key in self.store:
            del self.store[key]
            self.save()
            return f"Borrado {key}"
        return "Llave no encontrada"
    
db = RilooxDB()

print(r"""
    ____  _ __                    ____  ____ 
   / __ \(_) /___  ____  _  __   / __ \/ __ )
  / /_/ / / / __ \/ __ \| |/_/  / / / / __  |
 / _, _/ / / /_/ / /_/ />  <   / /_/ / /_/ / 
/_/ |_/_/_/\____/\____/_/|_|  /_____/_____/  
                                            
                    """)
while True:
    try:
        cmd = input("Que quieres hacer? (create/read/update/delete/exit): ").split()
    except (EOFError, KeyboardInterrupt):
        print(f"Hasta luego! :)")
        break

    if not cmd:
        continue

    if cmd[0] == "exit":
        print(f"Hasta luego! :)")
        break
    elif cmd[0] == "create":
        print(db.create(cmd[1], cmd[2]))
    elif cmd[0] == "read":
        print(db.read(cmd[1]))
    elif cmd[0] == "update":
        print(db.update(cmd[1], cmd[2]))
    elif cmd[0] == "delete":
        print(db.delete(cmd[1]))
    else:
        print("Comando Invalido! Prueba: create <key> <value>, read <key>, update <key> <value>, delete <key>, exit")
    
 