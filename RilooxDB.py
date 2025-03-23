# last modification: riloox 23/3/25
import pickle
from cryptography.fernet import Fernet

class RilooxDB:
    def __init__(self, key_file="secret.key", db_file="rilooxdb.pkl"):
        try:
            with open(key_file, "rb") as kf:
                key = kf.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(key_file, "wb") as kf:
                kf.write(key)
        self.cipher = Fernet(key)

        self.db_file = db_file
        self.store = {}
        self.load()

    def encrypt_value(self, value):
        return self.cipher.encrypt(str(value).encode('utf-8')).decode('utf-8')
    
    def decrypt_value(self, encrypted_value):
        try:
            return self.cipher.decrypt(encrypted_value.encode('utf-8')).decode('utf-8')
        except:
            return encrypted_value

    def load(self):
        try:
            with open(self.db_file, 'rb') as f:
                self.store = pickle.load(f)
        except (FileNotFoundError, pickle.PickleError, EOFError):
            self.store = {}

    def save(self):
        with open(self.db_file, 'wb') as f:
            pickle.dump(self.store, f)

    def execute_query(self, query):
        query = query.strip().upper()
        parts = query.split()

        try:
            if parts[0] == "INSERT":
                if "INTO" not in parts or "VALUES" not in parts:
                    return "Error de sintaxis: Usa INSERT INTO tabla VALUES ('llave', 'valor')"
                values_start = query.index("VALUES") + len("VALUES")
                values_str = query[values_start:].strip(" ()")
                key_value = [v.strip(" '") for v in values_str.split(",")]
                if len(key_value) != 2:
                    return "Error de sintaxis: VALUES deberia tener una llave y un valor"
                key, value = key_value
                encrypted_value = self.encrypt_value(value)
                self.store[key] = encrypted_value
                self.save()
                return "INSERT ejecutado satisfactoriamente!"
            
            elif parts[0] == "SELECT":
                distinct = "DISTINCT" in parts
                select_idx = 1 if not distinct else 2
                selected_column = parts[select_idx]
                if selected_column not in ["*", "KEY", "VALUE"]:
                    return "Error de sintaxis: Solo SELECT *, SELECT KEY o SELECT VALUE soportados actualmente."
                
                where_clause = None
                if "WHERE" in parts:
                    where_idx = parts.index("WHERE")
                    where_clause = " ".join(parts[where_idx + 1:])
                
                results = []
                seen_keys = set()

                # Fixed typo: encrpyed_value -> encrypted_value
                for key, encrypted_value in self.store.items():
                    decrypted_value = self.decrypt_value(encrypted_value)  # Now uses correct variable
                    if where_clause:
                        condition = where_clause.split("=")
                        if len(condition) != 2:
                            return "Error de sintaxis en la clausula WHERE"
                        cond_key, cond_value = condition[0].strip(), condition[1].strip(" '")
                        if cond_key == "KEY" and key != cond_value:
                            continue
                        elif cond_key == "VALUE" and decrypted_value != cond_value:
                            continue

                    if selected_column == "*":
                        row = (key, decrypted_value)
                    elif selected_column == "KEY":
                        row = (key,)
                    elif selected_column == "VALUE":
                        row = (decrypted_value,)

                    if distinct:
                        if key not in seen_keys:
                            results.append(row)
                            seen_keys.add(key)
                    else:
                        results.append(row)
                    
                return results
            
            elif parts[0] == "DELETE":
                if "WHERE" not in parts:
                    return "Error de sintaxis: DELETE requiere clausula WHERE"
                where_clause = " ".join(parts[parts.index("WHERE") + 1:])
                condition = where_clause.split("=")
                if len(condition) != 2:
                    return "Error de sintaxis en la clausula WHERE"
                cond_key, cond_value = condition[0].strip(), condition[1].strip(" '")

                deleted = False
                if cond_key == "KEY" and cond_value in self.store:
                    del self.store[cond_value]
                    deleted = True
                elif cond_key == "VALUE":
                    for key, encrypted_value in list(self.store.items()):
                        if self.decrypt_value(encrypted_value) == cond_value:
                            del self.store[key]
                            deleted = True
                if deleted:
                    self.save()
                return "Entrada borrada satisfactoriamente" if deleted else "No se encontró la entrada"
            
            elif parts[0] == "UPDATE":
                if "SET" not in parts or "WHERE" not in parts:
                    return "Error de sintaxis, usar UPDATE table SET value = 'valor' WHERE key = 'llave'"
                
                set_idx = parts.index("SET")
                where_idx = parts.index("WHERE")
                set_clause = " ".join(parts[set_idx + 1:where_idx])
                if set_clause.split("=")[0].strip() != "VALUE":
                    return "Error de sintaxis: Solo se soporta 'SET value' actualmente"
                new_value = set_clause.split("=")[1].strip(" '")
                encrypted_new_value = self.encrypt_value(new_value)

                where_clause = " ".join(parts[where_idx + 1:])
                condition = where_clause.split("=")
                if len(condition) != 2:
                    return "Error de sintaxis en la clausula WHERE"
                cond_key, cond_value = condition[0].strip(), condition[1].strip(" '")

                updated = False
                if cond_key == "KEY" and cond_value in self.store:
                    self.store[cond_value] = encrypted_new_value
                    updated = True
                elif cond_key == "VALUE":
                    for key, encrypted_value in list(self.store.items()):
                        if self.decrypt_value(encrypted_value) == cond_value:
                            self.store[key] = encrypted_new_value
                            updated = True
                if updated:
                    self.save()
                return "Consulta ejecutada correectamente" if updated else "No se encontró la entrada"
            
            else:
                return "Consulta no soportada por RilooxDB (aún, probablemente.)"
        
        except Exception as e:
            return f"Error: {str(e)}"

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
        query = input("Insertar query SQL :D (o 'exit' para salir o_o): ").strip()
        if query.lower() == "exit":
            print("Hasta luego, diviertete :)")
            break

        result = db.execute_query(query)

        if isinstance(result, str):
            print(result)
        else:
            for row in result:
                print(row)
    
    except (EOFError, KeyboardInterrupt):
        print("Hasta luego, diviertete :)")
        break
    except Exception as e:
        print(f"Error: {str(e)}")