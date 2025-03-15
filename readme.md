# RilooxDB

**A Simple Encrypted Key-Value Database in Python**

RilooxDB is a basic, in-memory key-value store with file persistence and encryption, built as a personal learning project to explore how databases work under the hood. Created on March 15, 2025, this tool helped me dive into core database concepts like CRUD operations, persistence, error handling, and encryption—all in a simple, command-line package.

## Features
- **Key-Value Storage**: Store data as key-value pairs (e.g., `"name": "Alice"`).
- **CRUD Operations**: Create, Read, Update, and Delete entries via simple commands.
- **Persistence**: Saves data to an encrypted JSON file (`rilooxdb.json`).
- **Encryption**: Uses Fernet (AES-128) from the `cryptography` library to secure data.
- **Command-Line Interface**: Interactive CLI with ASCII art for a fun touch.
- **Error Handling**: Robust against empty inputs, interrupts (`Ctrl+C`), EOF (`Ctrl+Z`), and encryption mismatches.

## Purpose
I built RilooxDB to learn:
- How databases manage data in memory and on disk.
- Basics of file I/O and JSON serialization in Python.
- Encryption fundamentals with Fernet (key generation, encryption/decryption).
- Exception handling for user inputs and file operations.
- Structuring a small Python project with a class-based design.

It’s not meant for production use—just a sandbox to experiment with database ideas!

## Installation
1. **Clone the Repository** (if hosted):
   ```bash
   git clone https://github.com/yourusername/rilooxdb.git
   cd rilooxdb
   ```
2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install cryptography
   ```
4. **Run It**:
   ```bash
   python RilooxDB.py
   ```

## Usage
Run the script, and you’ll see an ASCII banner followed by a prompt:
```
    ____  _ __                    ____  ____ 
   / __ \(_) /___  ____  _  __   / __ \/ __ )
  / /_/ / / / __ \/ __ \| |/_/  / / / / __  |
 / _, _/ / / /_/ / /_/ />  <   / /_/ / /_/ / 
/_/ |_/_/_/\____/\____/_/|_|  /_____/_____/  
                                            
Que quieres hacer? (create/read/update/delete/exit): 
```

### Commands
- **`create <key> <value>`**: Add a key-value pair (e.g., `create name Alice`).
- **`read <key>`**: Retrieve a value (e.g., `read name`).
- **`update <key> <value>`**: Update an existing key (e.g., `update name Bob`).
- **`delete <key>`**: Remove a key (e.g., `delete name`).
- **`exit`**: Quit the program (also works with `Ctrl+C` or `Ctrl+Z`).

### Example
```
> create name Alice
Guardado name con valor Alice
> read name
Alice
> update name Bob
Actualizado name a valor Bob
> delete name
Borrado name
> read name
Llave no encontrada
> exit
Hasta luego! :)
```

## How It Works
- **Storage**: Data lives in a Python dictionary (`self.store`) in memory.
- **Persistence**: On each CRUD operation, the dictionary is serialized to JSON, encrypted with Fernet, and saved to `rilooxdb.json`.
- **Encryption**: A key is generated and stored in `secret.key` (created if missing). Fernet ensures the data file is secure.
- **Loading**: On startup, it decrypts `rilooxdb.json` (if present) or starts fresh if the file is missing or invalid.

## What I Learned
- **CRUD Basics**: Implementing Create, Read, Update, Delete operations taught me the core of database functionality.
- **File I/O**: Reading/writing binary data for encryption vs. text for JSON.
- **Encryption**: Using Fernet to secure data, handling keys, and dealing with `InvalidToken` errors when keys mismatch.
- **Error Handling**: Managing `EOFError`, `KeyboardInterrupt`, and empty inputs to keep the program robust.
- **Python**: Classes, exception handling, and string manipulation for the CLI.

## Limitations
- In-memory only (no indexing or querying beyond key lookups).
- No concurrency support (single-user only).
- Simple key-value model—no complex data structures.
- Overwrites the entire file on every save (inefficient for large datasets).

## Future Ideas
- Add a query language for filtering data.
- Use a log-based approach instead of overwriting the whole file.
- Support concurrent access with threading.
- Experiment with other encryption methods (e.g., AES directly).

## Files
- **`RilooxDB.py`**: The main script with the database logic.
- **`rilooxdb.json`**: Encrypted data file (generated on save).
- **`secret.key`**: Encryption key (generated on first run—keep it safe!).

## License
This is a learning project, so feel free to use or modify it however you like—no formal license, just don’t blame me if it eats your data! 😄

## Acknowledgments
- Built with help from xAI’s Grok, who guided me through debugging and encryption.
- Inspired by my curiosity about how SQLite or Redis might work at a basic level.

---

### Notes for You
- **Personalize It**: Add your name or GitHub handle if you share it!
- **Spanish Touch**: I kept some Spanish phrases (`"Hasta luego! :)"`, `"Guardado"`) to match your code—adjust if you want full English or more Spanish.
- **Expand**: If you add features (e.g., a GUI), update the README accordingly.