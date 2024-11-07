import sqlite3

def connect_db():
    return sqlite3.connect('sua_base_de_dados.db')

def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password BLOB,
                role TEXT
            )
        ''')

        # Tabela de agendamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Agendamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                professor_name TEXT,
                date TEXT,
                start_time TEXT,
                end_time TEXT,
                client_name TEXT,
                subject TEXT,
                FOREIGN KEY(professor_name) REFERENCES Usuarios(username)
            )
        ''')

        conn.commit()


def list_appointments(professor_name):
    """Recupera todos os agendamentos de um professor específico."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Agendamento WHERE professor_name = ?", (professor_name,))
        appointments = cursor.fetchall()
        return appointments


def cancel_appointment(appointment_id):
    """Cancela um agendamento pelo ID."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Agendamento WHERE id = ?", (appointment_id,))
        conn.commit()
        return f"Agendamento com ID {appointment_id} cancelado com sucesso!"


def list_professors():
    """Recupera uma lista de todos os professores cadastrados."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Usuarios WHERE role = 'professor'")
        return [row[0] for row in cursor.fetchall()]


def list_appointments_for_user(client_name):
    """Recupera uma lista de agendamentos para um cliente específico."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, professor_name, date, start_time, end_time, subject FROM Agendamento WHERE client_name = ?",
            (client_name,)
        )
        return cursor.fetchall()