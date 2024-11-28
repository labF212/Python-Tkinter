import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.animation as animation
import random

# Configuração inicial
num_amostras = 100
recolher_dados = True  # Controla se os dados estão sendo recolhidos

# Função para gerar dados aleatórios
def gerar_dados():
    temperatura = random.uniform(0, 100)  # Temperatura em graus Celsius
    humidade = random.uniform(0, 100)     # Humidade em porcentagem
    return temperatura, humidade

# Inicializar listas de dados
tempos = list(range(num_amostras))
temperaturas = [0] * num_amostras
humidades = [0] * num_amostras

# Função para atualizar o gráfico
def atualizar(frame):
    global temperaturas, humidades, recolher_dados
    if recolher_dados:
        # Obter novos valores e remover os antigos
        nova_temp, nova_hum = gerar_dados()
        temperaturas.pop(0)
        humidades.pop(0)
        temperaturas.append(nova_temp)
        humidades.append(nova_hum)

    # Atualizar os dados do gráfico
    linha_temperatura.set_ydata(temperaturas)
    linha_humidade.set_ydata(humidades)
    return linha_temperatura, linha_humidade

# Função para alternar recolha de dados
def alternar_recolha(event):
    global recolher_dados
    recolher_dados = not recolher_dados
    botao.label.set_text("Iniciar" if not recolher_dados else "Parar")

# Configuração do gráfico
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Ajustar para o botão
ax.set_xlim(0, num_amostras - 1)
ax.set_ylim(0, 100)
ax.set_title("Temperatura e Humidade em Tempo Real")
ax.set_xlabel("Tempo (amostras)")
ax.set_ylabel("Valor")

# Inicializar linhas do gráfico
linha_temperatura, = ax.plot(tempos, temperaturas, label="Temperatura (°C)", color='red')
linha_humidade, = ax.plot(tempos, humidades, label="Humidade (%)", color='blue')
ax.legend(loc="upper right")

# Configurar botão
ax_botao = plt.axes([0.45, 0.05, 0.1, 0.075])  # Posição [esquerda, baixo, largura, altura]
botao = Button(ax_botao, "Parar")
botao.on_clicked(alternar_recolha)

# Configurar animação
ani = animation.FuncAnimation(fig, atualizar, interval=500, blit=True)

plt.show()
