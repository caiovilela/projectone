from database import connect_db

def add_professor(nome, professor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Professores (id, nome) VALUES (?, ?)", (professor_id, nome))
    conn.commit()
    conn.close()

def list_professors():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Professores")
    professors = cursor.fetchall()
    conn.close()
    return professors

def clear_professors():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Professores")  
    conn.commit()
    conn.close()


