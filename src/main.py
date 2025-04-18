import sqlite3
from tkinter import messagebox
import os

class system_register:

    def __init__(self):
        db_folder = 'database'
        db_file = 'students.db'
        db_path = os.path.join(db_folder, db_file)
        
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)

        if not os.path.exists(db_path):
            messagebox.showwarning("Aviso", f"O banco de dados '{db_file}' não foi encontrado. Um novo será criado.")

        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS students(
                Id INTEGER PRIMARY KEY AUTOINCREMENT, 
                Idade TEXT NOT NULL,
                Nome TEXT NOT NULL,
                Email TEXT NOT NULL,
                Sexo TEXT NOT NULL,
                Data_Nasc TEXT NOT NULL,
                Curso TEXT NOT NULL,
                Img TEXT NOT NULL)""")

    def register_student(self, students):
        try:
            self.c.execute("INSERT INTO students(Idade, Nome, Email, Sexo, Data_Nasc, Curso, Img) VALUES(?,?,?,?,?,?,?)", students)
            self.conn.commit()
            last_row_id = self.c.lastrowid
            if last_row_id:
                messagebox.showinfo('Sucesso!', 'Você foi cadastrado com sucesso!')
                return True
            else:
                messagebox.showerror("Erro!", "Falha ao verificar o sucesso do cadastro.")
                return False
        except (Exception, sqlite3.Error) as e:
            messagebox.showerror("Erro!", str(e))

    def view_all_students(self):
        try:
            self.c.execute("SELECT * FROM students")
            dados = self.c.fetchall()
            return dados
        except Exception as e:
            messagebox.showerror('Erro', str(e))
            return []

    def search_student(self, id):
        try:
            self.c.execute("SELECT * FROM students WHERE Id = ?", (id,))
            dados_id = self.c.fetchone()
            if dados_id:
                return dados_id
            messagebox.showinfo('Erro', 'Não foi encontrado nenhum estudante com esse id!')
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def att_student(self, new_values):
        try:
            self.c.execute("SELECT * FROM students WHERE Id = ?", (new_values[-1],))
            dados_id = self.c.fetchone()
            if not dados_id:
                messagebox.showinfo('Erro', 'Não foi encontrado nenhum estudante com esse id!')
                return
            self.c.execute("UPDATE students SET Idade=?, Nome=?, Email=?, Sexo=?, Data_Nasc=?, Curso=?, Img = ? WHERE Id = ?", (new_values))
            self.conn.commit()
            messagebox.showinfo('Sucesso', f'O estudante de id:{new_values[-1]}, e suas informações foram atualizadas com sucesso!')
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def del_student(self, id):
        try:
            self.c.execute("DELETE FROM students WHERE Id = ?", (id,))
            self.conn.commit()
            messagebox.showinfo('Sucesso', f'O estudante de id {id} foi removido com sucesso!')
        except Exception as e:
            messagebox.showerror('Erro', str(e))

if __name__ == "__main__":
    call_class = system_register()
