import tkinter as tk  # Importa o tkinter
from tkinter import ttk  # Para usar a tabela
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random

# Configuração inicial
num_amostras = 100
recolher_dados = True

# Função para gerar dados aleatórios
def gerar_dados():
    temperatura = random.uniform(0, 100)
    humidade = random.uniform(0, 100)
    return temperatura, humidade

# Inicializar listas de dados
tempos = list(range(num_amostras))
temperaturas = [0] * num_amostras
humidades = [0] * num_amostras

# Função para atualizar a tabela
def atualizar_tabela():
    tabela.delete(*tabela.get_children())
    for i in range(len(temperaturas)):
        tabela.insert("", "end", values=(i, f"{temperaturas[i]:.2f}", f"{humidades[i]:.2f}"))

# Função para atualizar o gráfico
def atualizar(frame):
    global temperaturas, humidades, recolher_dados
    if recolher_dados:
        nova_temp, nova_hum = gerar_dados()
        temperaturas.pop(0)
        humidades.pop(0)
        temperaturas.append(nova_temp)
        humidades.append(nova_hum)
        atualizar_tabela()
    linha_temperatura.set_ydata(temperaturas)
    linha_humidade.set_ydata(humidades)
    return linha_temperatura, linha_humidade

# Função para alternar recolha de dados
def alternar_recolha():
    global recolher_dados
    recolher_dados = not recolher_dados
    botao_parar_iniciar.config(text="Iniciar" if not recolher_dados else "Parar")

# Função para sair da aplicação
def sair_aplicacao():
    janela.destroy()

# Criar a janela principal
janela = tk.Tk()
janela.title("Gráfico com Tabela de Dados")

# Divisão da janela
frame_grafico = tk.Frame(janela)
frame_grafico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_tabela = tk.Frame(janela)
frame_tabela.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Gráfico
fig, ax = plt.subplots()
ax.set_xlim(0, num_amostras - 1)
ax.set_ylim(0, 100)
ax.set_title("Temperatura e Humidade em Tempo Real")
ax.set_xlabel("Tempo (amostras)")
ax.set_ylabel("Valor")
linha_temperatura, = ax.plot(tempos, temperaturas, label="Temperatura (°C)", color='red')
linha_humidade, = ax.plot(tempos, humidades, label="Humidade (%)", color='blue')
ax.legend(loc="upper right")

canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Tabela de dados
colunas = ("Amostra", "Temperatura (°C)", "Humidade (%)")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, minwidth=0, width=120, stretch=tk.NO)
tabela.pack(fill=tk.BOTH, expand=True)

# Botões
botao_parar_iniciar = tk.Button(janela, text="Parar", command=alternar_recolha)
botao_parar_iniciar.pack(side=tk.BOTTOM, pady=10)

botao_sair = tk.Button(janela, text="Sair", command=sair_aplicacao)
botao_sair.pack(side=tk.BOTTOM, pady=10)

# Animação corrigida
ani = animation.FuncAnimation(fig, atualizar, interval=500, blit=True, save_count=num_amostras)

# Loop principal
janela.mainloop()
