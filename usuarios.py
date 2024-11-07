import bcrypt
import sqlite3
from database import connect_db  
def add_usuario(username, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    senha_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO Usuarios (username, password, role) VALUES (?, ?, ?)", (username, senha_hash, role))
    conn.commit()
    conn.close()

def autenticar_usuario(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role FROM Usuarios WHERE username = ?", (username,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario[1]):
        return {"username": usuario[0], "role": usuario[2]}
    return None

def authenticate_user(username, password):
    """Autentica o usuário e retorna o papel (role) ou None se falhar."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM Usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            stored_password, role = user
            
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                return role  
    return None  
