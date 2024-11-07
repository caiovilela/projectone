import sqlite3

def create_tables():
    with sqlite3.connect('sua_base_de_dados.db') as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Agendamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                professor_name TEXT,
                date TEXT,
                start_time TEXT,
                end_time TEXT,
                client_name TEXT,
                subject TEXT
            )
        ''')
        conn.commit()

def schedule_appointment(professor_name, date, start, end, client_name, subject):
    
    with sqlite3.connect('sua_base_de_dados.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE username = ? AND role = 'professor'", (professor_name,))
        professor = cursor.fetchone()

        if not professor:
            return "Professor não encontrado."

        
        cursor.execute("SELECT * FROM Agendamento WHERE professor_name = ? AND date = ? AND (start_time < ? AND end_time > ?)", 
                       (professor_name, date, end, start))
        if cursor.fetchone():
            return "Horário já está ocupado."

        
        cursor.execute("INSERT INTO Agendamento (professor_name, date, start_time, end_time, client_name, subject) VALUES (?, ?, ?, ?, ?, ?)", 
                       (professor_name, date, start, end, client_name, subject))
        conn.commit()
        
    return "Agendamento realizado com sucesso."

def list_appointments_for_professor(professor_name):
    with sqlite3.connect('sua_base_de_dados.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Agendamento WHERE professor_name = ?", (professor_name,))
        return cursor.fetchall()

def list_professors():
    with sqlite3.connect('sua_base_de_dados.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Usuarios WHERE role = 'professor'")
        professors = cursor.fetchall()
    return [prof[0] for prof in professors]



def list_user_appointments(username):
    try:
        conn = sqlite3.connect('sua_base_de_dados.db')  
        cursor = conn.cursor()

        
        cursor.execute("SELECT id, subject FROM Agendamento WHERE client_name = ?", (username,))
        appointments = cursor.fetchall()

        return [f"{row[0]}: {row[1]}" for row in appointments]  

    except Exception as e:
        return []
    finally:
        conn.close()



