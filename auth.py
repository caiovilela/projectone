import sqlite3
import bcrypt

def create_tables():
    with sqlite3.connect('sua_base_de_dados.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password BLOB,
                role TEXT
            )
        ''')
        conn.commit()

def create_user(username, password, is_professor):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    role = 'professor' if is_professor else 'usuario'
    
    try:
        with sqlite3.connect('sua_base_de_dados.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Usuarios (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    with sqlite3.connect('sua_base_de_dados.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM Usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            return result[1]  
    return None
