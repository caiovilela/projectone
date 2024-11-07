import tkinter as tk
from tkinter import messagebox, ttk
import bcrypt
from usuarios import authenticate_user, add_usuario
from agendamento import schedule_appointment, list_appointments_for_professor
from database import create_tables, list_professors, list_appointments, cancel_appointment, list_appointments_for_user

# Inicializando as tabelas
create_tables()

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Agendamento")
        self.user_role = None
        self.username = None
        self.screen_history = []
        self.login_screen()

    def go_back(self):
        if len(self.screen_history) > 1:
            self.screen_history.pop()
            last_screen = self.screen_history[-1]
            self.clear_frame()
            last_screen()

    def add_to_history(self, screen_function):
        """Adiciona uma tela ao histórico, se não for a última no histórico."""
        if not self.screen_history or self.screen_history[-1] != screen_function:
            self.screen_history.append(screen_function)

    def login_screen(self):
        """Tela de login."""
        self.add_to_history(self.login_screen) 

        tk.Label(self.root, text="Login").pack()
        tk.Label(self.root, text="Usuário:").pack()
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        tk.Label(self.root, text="Senha:").pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Registrar", command=self.show_register_screen).pack()
        

    def show_register_screen(self):
        """Tela de registro de novo usuário."""
        self.add_to_history(self.show_register_screen)
        self.clear_frame()

        tk.Label(self.root, text="Registrar Usuário").pack()
        tk.Label(self.root, text="Usuário:").pack()
        self.entry_reg_username = tk.Entry(self.root)
        self.entry_reg_username.pack()

        tk.Label(self.root, text="Senha:").pack()
        self.entry_reg_password = tk.Entry(self.root, show="*")
        self.entry_reg_password.pack()

        tk.Label(self.root, text="Você é um professor?").pack()
        self.is_professor_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Sim", variable=self.is_professor_var).pack()

        tk.Button(self.root, text="Registrar", command=self.register_user).pack()
        tk.Button(self.root, text="Voltar", command=self.go_back).pack()
        

    def register_user(self):
        """Registra o usuário no sistema."""
        username = self.entry_reg_username.get()
        password = self.entry_reg_password.get()
        is_professor = self.is_professor_var.get()

        if not username or not password:
            messagebox.showerror("Erro", "Porfavor preencha todos os campos.")
            return

        role = "professor" if is_professor else "usuario"

        add_usuario(username, password, role)
        messagebox.showinfo("Registro", "Usuário registrado com sucesso!")
        self.clear_frame()
        self.login_screen()

    def login(self):
        """Autentica o usuário e exibe o menu principal com base no perfil."""
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Erro"," Porfavor preencha todos os campos.")
            return
        
        role = authenticate_user(username, password)

        if role:
            self.user_role = role
            self.username = username
            self.show_main_menu()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

    def show_user_appointments(self):
        """Tela de visualização de agendamentos para o usuário."""
        self.add_to_history(self.show_user_appointments)
        self.clear_frame()

        tk.Label(self.root, text="Meus Agendamentos").pack()
        
        appointments = list_appointments_for_user(self.username)

        if appointments:
            for appointment in appointments:
                appt_text = f"Professor: {appointment[1]}, Data: {appointment[2]}, " \
                            f"Início: {appointment[3]}, Fim: {appointment[4]}, Assunto: {appointment[5]}"
                tk.Label(self.root, text=appt_text).pack()
        else:
            tk.Label(self.root, text="Nenhum agendamento encontrado.").pack()

        tk.Button(self.root, text="Voltar", command=self.go_back).pack()
        

    def show_main_menu(self):
        """Exibe o menu principal, com opções baseadas no perfil do usuário."""
        
        self.clear_frame()

        if self.user_role == "professor":
            tk.Button(self.root, text="Ver Agendamentos", command=self.show_appointments).pack()
            tk.Button(self.root, text="Cancelar Agendamento", command=self.cancel_appointment_screen).pack()
            tk.Button(self.root, text="Agendar Horário", command=self.schedule_screen).pack()
        elif self.user_role == "usuario":
            tk.Button(self.root, text="Agendar Horário", command=self.schedule_screen).pack()
            tk.Button(self.root, text="Ver Meus Agendamentos", command=self.show_user_appointments).pack()

        tk.Button(self.root, text="Sair", command=self.logout).pack()
        self.add_to_history(self.show_main_menu)

    def schedule_screen(self):
        """Tela de agendamento de horário."""
        self.add_to_history(self.schedule_screen)
        self.clear_frame()

        tk.Label(self.root, text="Agendar Horário").pack()
        tk.Label(self.root, text="Nome do Professor:").pack()

        self.professor_name = ttk.Combobox(self.root)
        self.professor_name['values'] = list_professors()
        self.professor_name.pack()

        tk.Label(self.root, text="Data (DD-MM-YYYY):").pack()
        self.appointment_date = tk.Entry(self.root)
        self.appointment_date.pack()

        tk.Label(self.root, text="Hora de Início (HH:MM):").pack()
        self.start_time = tk.Entry(self.root)
        self.start_time.pack()

        tk.Label(self.root, text="Hora de Fim (HH:MM):").pack()
        self.end_time = tk.Entry(self.root)
        self.end_time.pack()

        tk.Label(self.root, text="Seu Nome:").pack()
        self.client_name = tk.Entry(self.root)
        self.client_name.pack()

        tk.Label(self.root, text="Assunto:").pack()
        self.subject = tk.Entry(self.root)
        self.subject.pack()

        tk.Button(self.root, text="Confirmar Agendamento", command=self.confirm_schedule).pack()
        tk.Button(self.root, text="Voltar", command=self.go_back).pack()

    def confirm_schedule(self):
        """Confirma o agendamento."""
        professor_name = self.professor_name.get()
        date = self.appointment_date.get()
        start = self.start_time.get()
        end = self.end_time.get()
        client_name = self.client_name.get()
        subject = self.subject.get()

        result = schedule_appointment(professor_name, date, start, end, client_name, subject)
        
        messagebox.showinfo("Resultado", result)
        self.show_main_menu()
        

    def show_appointments(self):
        """Exibe os agendamentos de um professor."""
        self.add_to_history(self.show_appointments)
        self.clear_frame()

        tk.Label(self.root, text="Ver Agendamentos").pack()
        tk.Label(self.root, text="Nome do Professor:").pack()
        self.professor_name = tk.Entry(self.root)
        self.professor_name.pack()

        tk.Button(self.root, text="Buscar Agendamentos", command=self.view_appointments).pack()
        tk.Button(self.root, text="Voltar", command=self.go_back).pack()

    def view_appointments(self):
        """Mostra os detalhes de agendamentos do professor."""
        professor_name = self.professor_name.get()
        appointments = list_appointments_for_professor(professor_name)

        if appointments:
            for appointment in appointments:
                tk.Label(self.root, text=f"{appointment}").pack()
        else:
            messagebox.showinfo("Informação", "Nenhum agendamento encontrado para esse professor.")

    def cancel_appointment_screen(self):
        self.clear_frame()
        self.add_to_history(self.cancel_appointment_screen)  

        tk.Label(self.root, text="Cancelar Agendamento").pack()
        tk.Label(self.root, text="Selecione o Agendamento:").pack()

    
        self.appointment_selection = ttk.Combobox(self.root)
        appointments = list_appointments(self.username)  
        self.appointment_selection['values'] = [appt[0] for appt in appointments] 
        self.appointment_selection.pack()

        tk.Button(self.root, text="Confirmar Cancelamento", command=self.confirm_cancel_appointment).pack()
        tk.Button(self.root, text="Voltar", command=self.go_back).pack()

    def confirm_cancel_appointment(self):
        """Confirma o cancelamento do agendamento."""
        appointment_id = self.appointment_selection.get()
        
        if appointment_id:
            result = cancel_appointment(appointment_id)
            messagebox.showinfo("Resultado", result)
            self.cancel_appointment_screen()
        else:
            messagebox.showerror("Erro", "Selecione um agendamento para cancelar.")

    def logout(self):
        """Faz o logout e limpa o histórico."""
        self.user_role = None
        self.username = None
        self.screen_history.clear()  
        self.clear_frame()
        self.login_screen()

    def clear_frame(self):
        """Limpa todos os widgets da tela atual."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
