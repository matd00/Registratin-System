import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import Frame
from tkinter import messagebox
import sqlite3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.main import system_register
from PIL import Image, ImageTk

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
call_class = system_register()

from tkcalendar import DateEntry

import re

janela = Tk()
janela.title('Registrar Aluno')
janela.geometry('910x700')
janela.resizable(False,False)
janela.configure(background="#F7EFE8")

Style = ttk.Style(janela)
Style.theme_use("clam")

janela.grid_rowconfigure(1, weight=1)
janela.grid_columnconfigure(0, weight=1)

frame_logo = Frame(janela, width=910, height = 48, bg="#7B4B3A")
frame_logo.grid(row=0, column=0, padx=0, pady=0, sticky = NSEW, columnspan=5)

frame_buttons = Frame(janela, width=200, height = 200, bg="#F7EFE8", relief=RAISED)
frame_buttons.grid(row=1, column=0, padx=1, pady=1, sticky = NSEW)

linha = ttk.Separator(frame_buttons, orient='vertical',)
linha.place(x=70, y=120, width=1)  

frame_details = Frame(janela, width=710, height = 300, bg="#F7EFE8", relief=SOLID)
frame_details.grid(row=1, column=4, padx=10, pady=1, sticky = NSEW)

frame_table = Frame(janela, width=910, height = 350, bg="#D3B8A3", relief=SOLID)
frame_table.grid(row=3, column=0, padx=1, pady=0, sticky = NSEW, columnspan=5)

global imagem, imagem1, imagem2, imagem_caminho

app_lg_path = os.path.join('assets', 'logo.png') 
app_lg = Image.open(app_lg_path)
app_lg = app_lg.resize((50, 50))
app_lg = ImageTk.PhotoImage(app_lg)
app_logo = Label(frame_logo, image=app_lg)
app_logo = Label(frame_logo , image = app_lg, text="Registro de Alunos", width = 910, compound=LEFT, anchor = NW, font= "CourierNew16bold 22", foreground = "#7B4B3A", background = "#F7EFE8")
app_logo.place(x=5, y= 0)

l_nome = Label(frame_details, text="Nome *", font="CourierNew16bold 10", bg="#F7EFE8", fg="#7B4B3A")
l_nome.place(x=10, y=10)
e_nome = Entry(frame_details, width=30)
e_nome.place(x=10, y=30)

l_idade = Label(frame_details, text="Idade *", font="CourierNew16bold 10", bg="#F7EFE8", fg="#7B4B3A")
l_idade.place(x=100, y=120)
e_idade = Entry(frame_details, width=5)
e_idade.place(x=100, y=140)

# Data de nascimento
l_data_nasc = Label(frame_details, text="Data de nascimento *", font="CourierNew16bold 10", bg="#F7EFE8", fg="#7B4B3A")
l_data_nasc.place(x=250, y=10)
e_data_nasc = DateEntry(frame_details, width=15, background='darkblue', foreground='white', borderwidth=2, year=2000)
e_data_nasc.place(x=250, y=30)

# Email
l_email = Label(frame_details, text="Email *", font="CourierNew16bold 10", bg="#F7EFE8", fg="#7B4B3A")
l_email.place(x=10, y=65)
e_email = Entry(frame_details, width=30)
e_email.place(x=10, y=85)

# Sexo
l_sexo = Label(frame_details, text="Sexo *", font="CourierNew16bold 10", bg="#F7EFE8", fg="#7B4B3A")
l_sexo.place(x=10, y=120)
combo_sexo = ttk.Combobox(frame_details, values=["M", "F", "Outro"], width=5)
combo_sexo.place(x=10, y=140)

#curso
l_curso = tk.Label(frame_details, text="Curso *", font="CourierNew16bold 10", bg="#F7EFE8", fg="#7B4B3A")
l_curso.place(x=250, y=65)
combo_curso = ttk.Combobox(frame_details, values=["Informática", "Administração", "Design", "Engenharia"], width=25)
combo_curso.place(x=250, y=85)

imagem_caminho = ''
def set_image():
    global imagem, imagem2, imagem_caminho
    
    try:
        if imagem2:
            imagem2.destroy()
    except NameError:
        pass
    
    imagem_caminho = fd.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if not imagem_caminho:
        messagebox.showinfo("Info", "Por favor, selecione um arquivo de imagem.")
        return

    original = Image.open(imagem_caminho)
    width, height = original.size
    ratio = min(180/width, 210/height)
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    

    imagem = original.resize((new_width, new_height))
    imagem = ImageTk.PhotoImage(imagem)
    
    img_frame = Frame(frame_details, width=190, height=220, bg="#D3B8A3", relief=SOLID, borderwidth=1)
    img_frame.place(x=480, y=10)
    
    imagem2 = Label(img_frame, image=imagem, bg="#D3B8A3")
    imagem2.image = imagem  
    imagem2.place(relx=0.5, rely=0.5, anchor=CENTER)

def init_image_placeholder():
    img_frame = Frame(frame_details, width=190, height=220, bg="#D3B8A3", relief=SOLID, borderwidth=1)
    img_frame.place(x=480, y=10)
    
    placeholder_text = Label(img_frame, text="Sem imagem", bg="#D3B8A3", fg="#7B4B3A")
    placeholder_text.place(relx=0.5, rely=0.5, anchor=CENTER)

#botao carrgar imagem
load_image = tk.Button(frame_details, text="Carregar imagem", command=set_image, width=20, 
                    compound=CENTER, anchor=CENTER, bg="#9d6a5e", fg="white", 
                    font=("Segoe UI", 11, "bold"))
load_image.place(x=480, y=240)


def mostrar_alunos():
    list_header = ["ID", "Idade", "Nome", "Email", "Sexo", "Data de nascimento", "Curso", "Img"]
    list_data = call_class.view_all_students()

    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#F7EFE8",
                    foreground="#3E2C23",
                    rowheight=30,
                    fieldbackground="#F7EFE8",
                    font=('Arial', 11))

    style.configure("Treeview.Heading",
                    font=('Arial', 12, 'bold'),
                    background="#D3B8A3",
                    foreground="#3E2C23",
)

    style.map('Treeview', background=[('selected', '#E6D6C8')])

    frame_table.grid_columnconfigure(0, weight=1)
    frame_table.grid_rowconfigure(0, weight=1)

    container = Frame(frame_table, bg="#F7EFE8")
    container.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)
    
    tree_aluno = ttk.Treeview(frame_table, columns=list_header, show="headings")

    vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree_aluno.yview)
    hsb = ttk.Scrollbar(frame_table, orient="horizontal", command=tree_aluno.xview)

    tree_aluno.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree_aluno.grid(column=0, row=0, sticky="nsew")
    vsb.grid(column=1, row=0, sticky="ns")
    hsb.grid(column=0, row=1, sticky="ew")

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)
    
    hd = ["w", "w", "w", "center", "center", "center", "w", "w"] # Adicionado um 'w' extra para a coluna "Img"
    h = [50, 50, 150, 200, 80, 150, 150, 80]
    
    for n, col in enumerate(list_header):
        tree_aluno.heading(col, text=col.title(), anchor=hd[n])
        tree_aluno.column(col, width=h[n], anchor=hd[n])

    for i, item in enumerate(list_data):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree_aluno.insert("", 'end', values=item, tags=(tag,))

    tree_aluno.tag_configure('evenrow', background="#F7EFE8")
    tree_aluno.tag_configure('oddrow', background="#EAD8C8")

def procurar_aluno():
    global imagem, imagem2, imagem_caminho
    try:
        id = int(e_search.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite um valor numérico.")
        e_search.delete(0,tk.END)
        return

    dados_aluno = call_class.search_student(id)
    
    if dados_aluno:

        e_idade.delete(0, tk.END)
        e_nome.delete(0, tk.END)
        e_email.delete(0, tk.END)
        combo_sexo.delete(0, tk.END)
        e_data_nasc.delete(0, tk.END)
        combo_curso.delete(0, tk.END)
        
        e_idade.insert(END, dados_aluno[1])
        e_nome.insert(END, dados_aluno[2])
        e_email.insert(END, dados_aluno[3])
        combo_sexo.insert(END, dados_aluno[4])
        e_data_nasc.insert(END, dados_aluno[5])
        combo_curso.insert(END, dados_aluno[6])

        imagem = dados_aluno[7]
        imagem_caminho = dados_aluno[7]

        original = Image.open(imagem_caminho)
        width, height = original.size
        ratio = min(180/width, 210/height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
    
        imagem = original.resize((new_width, new_height))
        imagem = ImageTk.PhotoImage(imagem)
    
        img_frame = Frame(frame_details, width=190, height=220, bg="#D3B8A3", relief=SOLID, borderwidth=1)
        img_frame.place(x=480, y=10)
    
        imagem2 = Label(img_frame, image=imagem, bg="#D3B8A3")
        imagem2.image = imagem  
        imagem2.place(relx=0.5, rely=0.5, anchor=CENTER)
        
    
    return

def remover_aluno():
    global imagem, imagem2, imagem_caminho
    
    dados_para_remover = int(e_search.get())
    confirm = messagebox.askyesno("Remover Aluno", "Realmente deseja remover esse aluno?")
    if not confirm:
        e_idade.delete(0, tk.END)
        e_nome.delete(0, tk.END)
        e_email.delete(0, tk.END)
        combo_sexo.delete(0, tk.END)
        e_data_nasc.delete(0, tk.END)
        combo_curso.delete(0, tk.END)
        return 

    try:
        remove = call_class.del_student(dados_para_remover)
        if remove:
            messagebox.showinfo("Sucesso", "Aluno removido com sucesso")
            e_search.delete(0, tk.END)
    except sqlite3.Error as e:
        messagebox.showerror(f"Erro", "Erro ao remover aluno, {e}")
    return

def atualizar_aluno():
    global imagem,imagem2,imagem_caminho
    
    idade = e_idade.get()
    nome = e_nome.get()
    email = e_email.get()
    sexo = combo_sexo.get()
    data_nasc = e_data_nasc.get()
    curso = combo_curso.get()
    id_aluno = e_search.get()
    
    dados_para_atualizar = (idade, nome, email, sexo, data_nasc, curso, imagem_caminho, id_aluno)
    
    if "" in (idade, nome, email, sexo, data_nasc, curso):
        messagebox.showerror('Erro', 'Preencha todos os campos!')
        return
    if not idade.isnumeric():
        messagebox.showerror('Erro', 'Idade deve ser um número!')
        return
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        messagebox.showerror('Erro', 'Email inválido!')
        return
    if not data_nasc:
        messagebox.showerror('Erro', 'Data de nascimento inválida!')
        return
    if not curso:
        messagebox.showerror('Erro', 'Curso inválido!')
        return
    if not imagem_caminho:
        messagebox.showerror('Erro', 'Imagem não foi selecionada!')
        return

    try:
        atualizar = call_class.att_student(dados_para_atualizar)
    except sqlite3.Error as e:
        messagebox.showerror(f"Erro", "Erro ao atualizar aluno, {e}")
    
    if atualizar:
        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")

frame_search = Frame(frame_buttons, width=180, height=50, bg="#F7EFE8", relief=RAISED)
frame_search.pack(padx=10, pady=10, fill=X)

l_nome = Label(frame_search, text="Procurar Aluno: (Enter ID)", font="CourierNew16bold 10", bg="#F7EFE8", fg="#7B4B3A")

l_nome.pack(pady=10)  

e_search = Entry(frame_search, width=15)
e_search.pack(pady=5)

botao_procurar = Button(frame_search, command = procurar_aluno  ,anchor = CENTER, overrelief= RIDGE, text="Procurar", font="CourierNew16bold 10", bg="#7B4B3A", fg="#F7EFE8")
botao_procurar.pack(pady=5)

def adcionar_aluno():
    global imagem_caminho
    
    idade = e_idade.get()
    nome = e_nome.get()
    email = e_email.get()
    sexo = combo_sexo.get()
    data_nasc = e_data_nasc.get()
    curso = combo_curso.get()
    
    
    if not imagem_caminho:
        messagebox.showerror('Erro', 'Por favor, carregue uma imagem!')
        return
    
    if "" in (idade, nome, email, sexo, data_nasc, curso):
        messagebox.showerror('Erro', 'Preencha todos os campos!')
        return
        
    if not idade.isnumeric():
        messagebox.showerror('Erro', 'Insira uma idade válida!')
        return
        
    if not nome.replace(" ", "").isalpha():
        messagebox.showerror('Erro', 'Insira um nome válido!')
        return
        
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        messagebox.showerror('Erro', 'Insira um email válido')
        return

    student_data = (idade, nome, email, sexo, data_nasc, curso, imagem_caminho)
    
    if call_class.register_student(student_data):
        #limpar os bgl
        e_idade.delete(0, tk.END)
        e_nome.delete(0, tk.END)
        e_email.delete(0, tk.END)
        combo_sexo.set("")
        e_data_nasc.delete(0, tk.END)
        combo_curso.set("")
        imagem_caminho = ''
        init_image_placeholder()
        mostrar_alunos() 

adcionar_icon_path = os.path.join('assets', 'img.png')
adcionar_icon = Image.open(adcionar_icon_path)
adcionar_icon = adcionar_icon.resize((20, 20))  
adcionar_icon = ImageTk.PhotoImage(adcionar_icon)
adcionar = tk.Button(frame_buttons, text="Adcionar", command = adcionar_aluno, width=15, 
                    compound=LEFT, anchor=CENTER, bg="#9d6a5e", fg="white", 
                    font=("Segoe UI", 11, "bold"))
adcionar.place(x=10, y=160)

remover = tk.Button(frame_buttons, text="Remover", command = remover_aluno, width=15, 
                    compound=CENTER, anchor=CENTER, bg="#9d6a5e", fg="white", 
                    font=("Segoe UI", 11, "bold"))
remover.place(x=10, y=200)


Atualizar = tk.Button(frame_buttons, text="Atualizar", command = atualizar_aluno, width=15, 
                    compound=CENTER, anchor=CENTER, bg="#9d6a5e", fg="white", 
                    font=("Segoe UI", 11, "bold"))
Atualizar.place(x=10, y=240)

def limpar_dados_interface():
    e_idade.delete(0, tk.END)
    e_nome.delete(0, tk.END)
    e_email.delete(0, tk.END)
    combo_sexo.delete(0, tk.END)
    e_data_nasc.delete(0, tk.END)
    combo_curso.delete(0, tk.END)
    
    img_frame = Frame(frame_details, width=190, height=220, bg="#D3B8A3", relief=SOLID, borderwidth=1)
    img_frame.place(x=480, y=10)
    
    placeholder_text = Label(img_frame, text="Sem imagem", bg="#D3B8A3", fg="#7B4B3A")
    placeholder_text.place(relx=0.5, rely=0.5, anchor=CENTER)

Limpar = tk.Button(frame_details, text="Limpar", command = limpar_dados_interface , width=15, 
                    compound=CENTER, anchor=CENTER, bg="#9d6a5e", fg="white", 
                    font=("Segoe UI", 11, "bold"))
Limpar.place(x=250, y=150)

init_image_placeholder()
mostrar_alunos()

def start_interface():
    global janela
    janela.mainloop()