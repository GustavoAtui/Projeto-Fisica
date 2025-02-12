import tkinter as tk
from tkinter import messagebox
from scipy.integrate import quad
from math import sqrt, sin, pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constantes
carga_elementar = 1.602e-19  # C
h = 6.626e-34  # J.s
hj = 4.136E-15
c = 3.00e8  # m/s
massa_eletron = 9.109e-31  # kg
massa_proton = 1.672e-27  # kg

def calcular():
    escolha = opcao_massa.get()
    opcoes = opcao_calculos.get()

    if escolha == 1:
        massa = massa_eletron
    elif escolha == 2:
        massa = massa_proton
    else:
        messagebox.showerror("Erro", "Escolha inválida.")
        return
    
    if opcoes == 1:
        campos = [entrada_L.get(), entrada_n_inicial.get(), entrada_n_final.get(), entrada_a.get(), entrada_b.get()]
        if "" in campos:
            messagebox.showerror("Erro", "Preencha todos os campos necessários.")
            return
        
        L = float(entrada_L.get())
        n_inicial = float(entrada_n_inicial.get())
        n_final = float(entrada_n_final.get())
        a = float(entrada_a.get())
        b = float(entrada_b.get())
        

        if a > L or b > L:
            messagebox.showerror("Erro", "Os valores de 'a' e 'b' devem ser menores à largura da caixa (L).")
            return

        kini = (n_inicial * np.pi) / L
        kfi = (n_final * np.pi) / L
        A = (2 / L) ** 0.5

        Eini = ((n_inicial * 2) * h * 2) / (8 * massa * (L ** 2))
        Efi = ((n_final * 2) * h * 2) / (8 * massa * (L ** 2))

        Efoton = abs((Efi - Eini) / carga_elementar)
        LambdaFoton = abs((hj * c) / Efoton)
        FrequenciaFoton = abs(c / LambdaFoton)

        veloini = sqrt((2 * Eini) / massa)
        velofi = sqrt((2 * Efi) / massa)

        lambdaini = (2 * L) / n_inicial
        lambdafi = (2 * L) / n_final
        def intinicial(x):
            return pow(np.sqrt(2/L) * np.sin(((n_inicial*np.pi)/L) * x),2)
        def intfinal(x):
            return pow(np.sqrt(2/L) * np.sin(((n_final*np.pi)/L) * x),2)

        probini = quad(intinicial, a, b)
        probfin = quad(intfinal, a, b)

        
        
        

        resultado_texto.set(f"A: {A:.3e}\n"
                            f"k {n_inicial:.0f}: {kini:.3e}\n"
                            f"k {n_final:.0f}: {kfi:.3e}\n"
                            f"---------------------------\n"
                            f"E {n_inicial:.0f} J: {Eini:.3e} J\n"
                            f"E {n_inicial:.0f} eV: {Eini / carga_elementar:.3e} eV\n"
                            f"E {n_final:.0f} J: {Efi:.3e} J\n"
                            f"E {n_final:.0f} eV: {Efi / carga_elementar:.3e} eV\n"
                            f"---------------------------\n"
                            f"E foton: {Efoton:.3e} eV\n"
                            f"Lambda Foton: {LambdaFoton:.3e} m\n"
                            f"Frequencia Foton: {FrequenciaFoton:.3e} Hz\n"
                            f"---------------------------\n"
                            f"Velocidade {n_inicial:.0f}: {veloini:.3e} v/m\n"
                            f"Velocidade {n_final:.0f}: {velofi:.3e} v/m\n"
                            f"---------------------------\n"
                            f"Comprimento {n_inicial:.0f}: {lambdaini:.3e} m\n"
                            f"Comprimento {n_final:.0f}: {lambdafi:.3e} m\n"
                            f"---------------------------\n"
                            f"Probabilidade {n_inicial:.0f}: {probini[0] * 100:.2f}%\n"
                            f"Probabilidade {n_final:.0f}: {probfin[0] * 100:.2f}%")
        xxx = np.linspace(0,L)
        psi_n1 = np.sqrt(2/L) * np.sin(n_inicial * np.pi * xxx / L)
        psi_n2 = np.sqrt(2/L) * np.sin(n_final * np.pi * xxx / L)

        # Criando gráficos focados no intervalo entre a e b
        plt.figure(figsize=(12, 8))

        # Gráfico para n inicial
        plt.subplot(211)
        plt.plot(xxx, psi_n1, color='blue')
        plt.title(f'Função de Onda para o Estado {n_inicial} entre $a$ e $b$')
        plt.xlabel('Posição ($x (Â)$)')
        plt.ylabel('Função de Onda ($\psi(x)$)')
        plt.legend()
        plt.grid(True)

        # Gráfico para n final
        plt.subplot(212)
        plt.plot(xxx, psi_n2, color='red')
        plt.title(f'Função de Onda para o Estado {n_final} entre $a$ e $b$')
        plt.xlabel('Posição ($x (Â)$)')
        plt.ylabel('Função de Onda ($\psi(x)$)')
        plt.legend()
        plt.grid(True)

        # Gráfico para a distribuição de probabilidade inicial e final
        plt.figure(2)
        prob_ni = np.sqrt((2/L) * np.power(np.sin((n_inicial * np.pi * xxx)/ L), 2))
        ninip = plt.subplot(211)
        ninip.set_title("Distribuição de probabilidade N Inicial")
        ninip.set_ylabel("y")
        ninip.set_xlabel("x (Â)")
        plt.plot(xxx, np.abs(prob_ni))

        prob_nf = np.sqrt((2 / L) * np.power(np.sin((n_final * np.pi * xxx) / L), 2))
        nfinp = plt.subplot(212)
        nfinp.set_title("Distribuição de probabilidade N Final")
        nfinp.set_ylabel("y")
        nfinp.set_xlabel("x (Â)")
        plt.plot(xxx, np.abs(prob_nf))
        plt.subplots_adjust(hspace=0.6)
    

        plt.tight_layout()
        

        def run_animation(transicoes):
            niveis = np.array([0, 0.2, 0.5, 0.9, 1.5])
            cores = ['blue', 'turquoise', 'lightpink', 'darkblue', 'cyan']
            
            fig, ax = plt.subplots()
            ax.set_xlim(-1, 6)
            ax.set_ylim(-0.1, 1.6)
            ax.set_ylabel('E (eV)')
            ax.set_xlabel('x (nm)')
            ax.set_xticks(np.arange(0, 6, 1))
            ax.set_yticks(niveis)
            ax.set_yticklabels([f'E{i+1}' for i in range(5)])
            
            for nivel, cor in zip(niveis, cores):
                ax.hlines(nivel, 0, 5, colors=cor, linestyles='-')
            
            particula, = ax.plot([], [], 'o', color='royalblue', markersize=10)
            onda, = ax.plot([], [], color='orange', alpha=0.5)
            base_onda_y = [0]
            
            texto = ax.text(0.1, -0.07, '', fontsize=12, va='center', ha='center', color='black')
            
            def init():
                particula.set_data([], [])
                onda.set_data([], [])
                texto.set_text('')
                return particula, onda, texto
            
            def animate(i):
                frame_transicao = i % 20
                indice_transicao = i // 20 % len(transicoes)
                inicio, fim = transicoes[indice_transicao]
                
                if frame_transicao < 10:
                    posicao_x = frame_transicao * 0.5
                    posicao_y = niveis[inicio]
                    onda.set_data([], [])
                    base_onda_y[0] = niveis[inicio]
                else:
                    posicao_x = 5
                    posicao_y = np.interp(frame_transicao - 10, [0, 9], [niveis[inicio], niveis[fim]])
                
                particula.set_data(posicao_x, posicao_y)
                
                if frame_transicao == 10 or frame_transicao > 10:
                    espalhamento = (frame_transicao - 10) * 0.1 if frame_transicao > 10 else 0
                    x_onda = np.linspace(5 - 0.5 - espalhamento, 5 + 0.5 + espalhamento, 100)
                    y_onda = base_onda_y[0] + np.sin((x_onda - 5) * 10) * 0.1 * (1 - espalhamento * 0.1)
                    onda.set_data(x_onda, y_onda)
                     
                if niveis[inicio] < niveis[fim]:
                    texto.set_text(f'Absorção de fóton: E{5-inicio} para E{5-fim}')
                else:
                    texto.set_text(f'Emissão de fóton: E{5-inicio} para E{5-fim} ')
                return particula, onda, texto
            
            ani = animation.FuncAnimation(fig, animate, frames=20 * len(transicoes),
                                        init_func=init, interval=100, blit=True)
            
            plt.show()

        # Exemplo de uso
        transicoes_usuario = [(1, 4), (4, 3), (3, 0), (0, 3), (3, 2), (2, 0), (0, 2), (2, 3), (3, 4), (4, 1), (1, 2)]
        run_animation(transicoes_usuario)


    elif opcoes == 2:
        campos = [entrada_Aa.get(), entrada_K.get(), entrada_x.get()]
        if "" in campos:
            messagebox.showerror("Erro", "Preencha todos os campos necessários.")
            return
        
        Aa = float(entrada_Aa.get())
        K = float(entrada_K.get())

        LL = 2 / (Aa ** 2)
        n = (K * LL) / pi

        xp = float(entrada_x.get())
        
        Prob_xp = pow(Aa * np.sin(K * xp * LL), 2)

        resultado_texto.set(f"Largura da Caixa: {LL:.3e} m\n"
                            f"Numero de onda: {n:.0f}\n"
                            f"---------------------------\n"
                            f"Valor de P(x) em dx: {Prob_xp:.3e} dx")
                        



root = tk.Tk()
root.title("Cálculos Quânticos")


frame_controles = tk.Frame(root)
frame_controles.pack(padx=20, pady=20)


opcao_massa = tk.IntVar()
opcao_massa.set(1)
tk.Label(frame_controles, text="Escolha a massa para os cálculos:").grid(row=0, column=0, sticky="w")
tk.Radiobutton(frame_controles, text="Massa do elétron", variable=opcao_massa, value=1).grid(row=1, column=0, sticky="w")
tk.Radiobutton(frame_controles, text="Massa do próton", variable=opcao_massa, value=2).grid(row=2, column=0, sticky="w")


opcao_calculos = tk.IntVar()
opcao_calculos.set(1)
tk.Label(frame_controles, text="Escolha o tipo de cálculo:").grid(row=3, column=0, sticky="w")
tk.Radiobutton(frame_controles, text="A partir do L, N inicial, N final, a, b :(a , b < L)", variable=opcao_calculos, value=1).grid(row=4, column=0, sticky="w")
tk.Radiobutton(frame_controles, text="A partir do A, K, x", variable=opcao_calculos, value=2).grid(row=5, column=0, sticky="w")


tk.Label(frame_controles, text="Largura da caixa (L):").grid(row=6, column=0, sticky="w")
entrada_L = tk.Entry(frame_controles)
entrada_L.grid(row=6, column=1)

tk.Label(frame_controles, text="n inicial da partícula:").grid(row=7, column=0, sticky="w")
entrada_n_inicial = tk.Entry(frame_controles)
entrada_n_inicial.grid(row=7, column=1)

tk.Label(frame_controles, text="n final da partícula:").grid(row=8, column=0, sticky="w")
entrada_n_final = tk.Entry(frame_controles)
entrada_n_final.grid(row=8, column=1)

tk.Label(frame_controles, text="Valor de a:").grid(row=9, column=0, sticky="w")
entrada_a = tk.Entry(frame_controles)
entrada_a.grid(row=9, column=1)

tk.Label(frame_controles, text="Valor de b:").grid(row=10, column=0, sticky="w")
entrada_b = tk.Entry(frame_controles)
entrada_b.grid(row=10, column=1)

tk.Label(frame_controles, text="A:").grid(row=11, column=0, sticky="w")
entrada_Aa = tk.Entry(frame_controles)
entrada_Aa.grid(row=11, column=1)

tk.Label(frame_controles, text="K:").grid(row=12, column=0, sticky="w")
entrada_K = tk.Entry(frame_controles)
entrada_K.grid(row=12, column=1)

tk.Label(frame_controles, text="x:").grid(row=13, column=0, sticky="w")
entrada_x = tk.Entry(frame_controles)
entrada_x.grid(row=13, column=1)

botao_calcular = tk.Button(frame_controles, text="Calcular", command=calcular)
botao_calcular.grid(row=14, columnspan=2, pady=10)

frame_resultado = tk.Frame(root)
frame_resultado.pack(padx=20, pady=20)

resultado_texto = tk.StringVar()
tk.Label(frame_resultado, text="Resultado:").pack()
label_resultado = tk.Label(frame_resultado, textvariable=resultado_texto)
label_resultado.pack()

root.mainloop()
