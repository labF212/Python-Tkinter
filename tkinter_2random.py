import tkinter as tk
from tkinter import ttk
from random import randint
from time import sleep, strftime
import threading
from datetime import datetime
from webbrowser import open

# Função para atualizar os valores aleatórios
def update():
    global temp, hum
    while True:
        sleep(0.5)
        temp = randint(0, 45)  # Simula a temperatura
        hum = randint(20, 80)  # Simula a umidade
        update_data()
        check_limits()

# Função para traduzir os meses para português
def translate_month(date_obj):
    date_month = date_obj.strftime("%B")
    months_eng = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    meses_pt = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    for i in range(len(months_eng)):
        if date_month == months_eng[i]:
            date_month = meses_pt[i]
            break
    return f"{date_obj.strftime('%d')} {date_month} {date_obj.strftime('%Y')}"

# Atualiza os valores na interface
def update_data():
    progress_temp['value'] = temp
    progress_hum['value'] = hum
    temp_label_value.config(text=f"{temp}ºC")
    hum_label_value.config(text=f"{hum}%")
    current_time = datetime.now()
    time_label_value.config(text=f"Hora Atual: {current_time.strftime('%H:%M:%S')}")
    date_label_value.config(text=translate_month(current_time))

# Verifica os limites e atualiza o LED
def check_limits():
    global hum
    val_min = int(spin_min.get())
    val_max = int(spin_max.get())

    if hum < val_min:
        label_rele.config(image=img_rele_offline)
        label_rele_text.config(text="Desligado")
    elif val_min <= hum <= val_max:
        label_rele.config(image=img_rele_on)
        label_rele_text.config(text="Ligado")
    else:
        label_rele.config(image=img_rele_high_hum)
        label_rele_text.config(text="Humidade Elevada")

# Janela Sobre
def show_about():
    about_window = tk.Toplevel(window)
    about_window.title("Sobre")
    about_window.geometry("300x150")
    
# Texto fixo
    tk.Label(
        about_window, 
        text="Sistema de Medida de Temperatura e Humidade\nVersão 1.0\nDesenvolvido por: Paulo Galvão", 
        font=("Arial", 10), 
        wraplength=380
    ).pack(pady=10)
    
    # Hiperligação
    def open_link(event):
        open("https://github.com/labF212/Python-Tkinter")
    
    link = tk.Label(
        about_window, 
        text="https://github.com/labF212/Python-Tkinter", 
        font=("Arial", 10), 
        fg="blue", 
        cursor="hand2"
    )
    link.pack()
    link.bind("<Button-1>", open_link)  # Clique com o botão esquerdo do rato

# Criar a janela principal
window = tk.Tk()
window.title("Leituras de Temperaturas e Humidade")

# Variáveis
temp = hum = 0

# Carregar as imagens
img_temp = tk.PhotoImage(file="temperatura.png")
img_hum = tk.PhotoImage(file="humidade.png")
img_rele_on = tk.PhotoImage(file="redon.png")
img_rele_offline = tk.PhotoImage(file="redoffline.png")
img_rele_high_hum = tk.PhotoImage(file="redoff.png")

# Criar menu
menu_bar = tk.Menu(window)
menu = tk.Menu(menu_bar, tearoff=0)
menu.add_command(label="Sobre", underline=0, command=show_about)
menu_bar.add_cascade(label="Menu", underline=0, menu=menu)
window.config(menu=menu_bar)

# Criar área de scroll
canvas = tk.Canvas(window, width=600, height=600)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Frame 1: Leitura de Dados
frame_leitura = tk.Frame(scrollable_frame, bg="grey", relief="ridge", bd=5)
frame_leitura.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

tk.Label(frame_leitura, text="Leitura de Dados", font=("Arial", 14), bg="grey").grid(row=0, column=0, columnspan=5, pady=5)

# Primeira linha: imagens e progressbars
tk.Label(frame_leitura, image=img_temp, bg="grey").grid(row=1, column=0, padx=10, pady=5)
progress_temp = ttk.Progressbar(frame_leitura, orient="vertical", length=110, maximum=50, style="custom.Horizontal.TProgressbar")
progress_temp.grid(row=1, column=1, padx=10)

tk.Label(frame_leitura, image=img_hum, bg="grey").grid(row=1, column=2, padx=10, pady=5)
progress_hum = ttk.Progressbar(frame_leitura, orient="vertical", length=110, maximum=100, style="custom.Horizontal.TProgressbar")
progress_hum.grid(row=1, column=3, padx=10)

# Segunda linha: textos e valores
tk.Label(frame_leitura, text="Temperatura", font=("Arial", 12), bg="grey").grid(row=2, column=0, pady=5)
temp_label_value = tk.Label(frame_leitura, text="0ºC", font=("Arial", 12), fg="red", bg="grey")
temp_label_value.grid(row=2, column=1, pady=5)

tk.Label(frame_leitura, text="Humidade", font=("Arial", 12), bg="grey").grid(row=2, column=2, pady=5)
hum_label_value = tk.Label(frame_leitura, text="0%", font=("Arial", 12), fg="blue", bg="grey")
hum_label_value.grid(row=2, column=3, pady=5)

# Linha contínua de separação
tk.Frame(frame_leitura, height=2, width=500, bg="black").grid(row=3, column=0, columnspan=5, pady=5)

# Linha com hora e data
time_label_value = tk.Label(frame_leitura, text="Hora Atual: 00:00:00", font=("Arial", 12), bg="grey", anchor="w")
time_label_value.grid(row=4, column=0, columnspan=3, pady=5, sticky="w")

date_label_value = tk.Label(frame_leitura, text="01 Janeiro 2000", font=("Arial", 12), bg="grey", anchor="e")
date_label_value.grid(row=4, column=3, pady=5, sticky="e")

# Frame 2: Tratamento de Dados
frame_tratamento = tk.Frame(scrollable_frame, bg="lightgrey", relief="ridge", bd=5)
frame_tratamento.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

tk.Label(frame_tratamento, text="Tratamento de Dados", font=("Arial", 14), bg="lightgrey").grid(row=0, column=0, columnspan=2, pady=5)

# Linha contínua de separação
tk.Frame(frame_tratamento, height=2, width=500, bg="black").grid(row=1, column=0, columnspan=2, pady=5)

# Coluna 0: Imagem do LED
label_rele = tk.Label(frame_tratamento, image=img_rele_offline, bg="lightgrey")
label_rele.grid(row=2, column=0, padx=10, pady=10)
label_rele_text = tk.Label(frame_tratamento, text="Desligado", font=("Arial", 12), bg="lightgrey")
label_rele_text.grid(row=3, column=0)

# Coluna 1: Configurações de limite de umidade
config_frame = tk.Frame(frame_tratamento, bg="lightgrey")
config_frame.grid(row=2, column=1, padx=10, pady=10)

tk.Label(config_frame, text="Configuração de limites de Humidade", font=("Arial", 12), bg="lightgrey").grid(row=0, column=0, columnspan=2, pady=5)

tk.Label(config_frame, text="Valor mínimo:", bg="lightgrey").grid(row=1, column=0, sticky="e", padx=5)
spin_min = tk.Spinbox(config_frame, from_=0, to=50, width=5)
spin_min.grid(row=1, column=1, sticky="w", padx=5)

tk.Label(config_frame, text="Valor máximo:", bg="lightgrey").grid(row=2, column=0, sticky="e", padx=5)
spin_max = tk.Spinbox(config_frame, from_=50, to=100, width=5)
spin_max.grid(row=2, column=1, sticky="w", padx=5)



# Estilo das barras de progresso
style = ttk.Style(window)
style.configure("custom.Horizontal.TProgressbar", thickness=20)

# Inicia thread para atualizar os valores
threading.Thread(target=update, daemon=True).start()

# Loop principal
window.mainloop()
