import tkinter as tk  # Importa o tkinter
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random

# Configuração inicial
num_amostras = 100
max_valores_tabela = 20  # Número máximo de valores na tabela
recolher_dados = True
num_amostra = 0  # Contador para o número de amostras

# Função para gerar dados aleatórios
def gerar_dados():
    temperatura = random.uniform(20, 25)
    humidade = random.uniform(20, 80)
    return temperatura, humidade

# Inicializar listas de dados
tempos = list(range(num_amostras))
temperaturas = [0] * num_amostras
humidades = [0] * num_amostras

# Função para atualizar o gráfico e a tabela
def atualizar(frame):
    global temperaturas, humidades, recolher_dados, num_amostra
    if recolher_dados:
        num_amostra += 1  # Incrementa o número da amostra
        nova_temp, nova_hum = gerar_dados()
        temperaturas.pop(0)
        humidades.pop(0)
        temperaturas.append(nova_temp)
        humidades.append(nova_hum)

        # Adiciona os novos dados à tabela
        tabela.insert("", "end", values=(num_amostra, f"{nova_temp:.2f}", f"{nova_hum:.2f}"))

        # Remove linhas antigas para manter o número fixo de valores na tabela
        if len(tabela.get_children()) > max_valores_tabela:
            tabela.delete(tabela.get_children()[0])

        # Estiliza as linhas da tabela (zebrado)
        for i, item in enumerate(tabela.get_children()):
            tabela.tag_configure('oddrow', background='lightgrey')
            tabela.tag_configure('evenrow', background='white')
            tabela.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow'))

    # Atualizar os gráficos
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
    janela.quit()  # Encerra o loop principal
    janela.destroy()  # Fecha a janela principal

# Função para criar tooltips
def criar_tooltip(widget, texto):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    tooltip_label = tk.Label(tooltip, text=texto, background="yellow", relief=tk.SOLID, borderwidth=1, font=("Helvetica", 8))
    tooltip_label.pack()

    def mostrar_tooltip(event):
        tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        tooltip.deiconify()

    def esconder_tooltip(event):
        tooltip.withdraw()

    widget.bind("<Enter>", mostrar_tooltip)
    widget.bind("<Leave>", esconder_tooltip)

# Criar a janela principal
janela = tk.Tk()
janela.title("Gráfico com Tabela de Dados")

# Divisão da janela
frame_grafico = tk.Frame(janela)
frame_grafico.grid(row=0, column=0, padx=10, pady=10)

frame_tabela = tk.Frame(janela)
frame_tabela.grid(row=0, column=1, padx=10, pady=10)

frame_botoes = tk.Frame(janela)
frame_botoes.grid(row=1, column=0, columnspan=2, pady=10)

# Gráfico
fig, ax = plt.subplots()
ax.set_xlim(0, num_amostras - 1)
ax.set_ylim(0, 110)
ax.set_title("Temperatura e Humidade em Tempo Real\n")
ax.set_xlabel("Tempo (amostras)")
ax.set_ylabel("Valor")

# Adicionar grelha horizontal
ax.grid(axis='y', color='lightgrey', linestyle='--', linewidth=0.7)

# Ajustar escala vertical para divisões de 10
ax.set_yticks(range(0, 101, 10))

# Desenhar as linhas
linha_temperatura, = ax.plot(tempos, temperaturas, label="Temperatura (°C)", color='red')
linha_humidade, = ax.plot(tempos, humidades, label="Humidade (%)", color='blue')

# Adicionar a legenda acima do gráfico
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=2)

canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Título da tabela
titulo_tabela = tk.Label(frame_tabela, text="Tabela de Recolha de Dados", font=("Helvetica", 12, "bold"))
titulo_tabela.pack(pady=5)

# Tabela de dados
colunas = ("Amostra", "Temperatura (°C)", "Humidade (%)")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=max_valores_tabela)
for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, minwidth=0, width=120, stretch=tk.NO)
tabela.pack(anchor="center", fill=tk.BOTH, expand=True)

# Botões
botao_parar_iniciar = tk.Button(frame_botoes, text="Parar", command=alternar_recolha)
botao_parar_iniciar.grid(row=0, column=0, padx=10)
criar_tooltip(botao_parar_iniciar, "Clique para iniciar ou parar a recolha de dados.")

botao_sair = tk.Button(frame_botoes, text="Sair", command=sair_aplicacao)
botao_sair.grid(row=0, column=1, padx=10)
criar_tooltip(botao_sair, "Clique para sair da aplicação.")

# Animação
ani = animation.FuncAnimation(fig, atualizar, interval=500, blit=True, save_count=num_amostras)

# Loop principal
janela.mainloop()
