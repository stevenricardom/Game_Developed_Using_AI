import tkinter as tk
from tkinter import messagebox
import math
import random

# Tablero inicial
tablero = [' ' for _ in range(9)]

# Jugadores
JUGADOR_HUMANO = 'X'
JUGADOR_IA = 'O'

# Función para verificar si hay un ganador
def hay_ganador(tablero, jugador):
    combinaciones_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]
    for combinacion in combinaciones_ganadoras:
        if all(tablero[pos] == jugador for pos in combinacion):
            return True
    return False

# Función para verificar si el tablero está lleno
def tablero_lleno(tablero):
    return ' ' not in tablero

# Función Minimax
def minimax(tablero, profundidad, es_maximizando):
    if hay_ganador(tablero, JUGADOR_IA):
        return 1
    elif hay_ganador(tablero, JUGADOR_HUMANO):
        return -1
    elif tablero_lleno(tablero):
        return 0

    if es_maximizando:
        mejor_valor = -math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = JUGADOR_IA
                valor = minimax(tablero, profundidad + 1, False)
                tablero[i] = ' '
                mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = JUGADOR_HUMANO
                valor = minimax(tablero, profundidad + 1, True)
                tablero[i] = ' '
                mejor_valor = min(mejor_valor, valor)
        return mejor_valor

# Función para que la IA haga su movimiento
def movimiento_ia(tablero):
    # Encontrar todos los movimientos óptimos
    mejores_movimientos = []
    mejor_valor = -math.inf
    for i in range(9):
        if tablero[i] == ' ':
            tablero[i] = JUGADOR_IA
            valor = minimax(tablero, 0, False)
            tablero[i] = ' '
            if valor > mejor_valor:
                mejor_valor = valor
                mejores_movimientos = [i]
            elif valor == mejor_valor:
                mejores_movimientos.append(i)
    # Elegir aleatoriamente entre los movimientos óptimos
    return random.choice(mejores_movimientos)

# Función para manejar el clic del jugador humano
def clic_jugador(pos):
    if tablero[pos] == ' ':
        tablero[pos] = JUGADOR_HUMANO
        botones[pos].config(text=JUGADOR_HUMANO, state=tk.DISABLED)
        if hay_ganador(tablero, JUGADOR_HUMANO):
            messagebox.showinfo("Fin del juego", "¡Ganaste!")
            reiniciar_juego()
        elif tablero_lleno(tablero):
            messagebox.showinfo("Fin del juego", "¡Empate!")
            reiniciar_juego()
        else:
            movimiento = movimiento_ia(tablero)
            tablero[movimiento] = JUGADOR_IA
            botones[movimiento].config(text=JUGADOR_IA, state=tk.DISABLED)
            if hay_ganador(tablero, JUGADOR_IA):
                messagebox.showinfo("Fin del juego", "¡La IA ganó!")
                reiniciar_juego()
            elif tablero_lleno(tablero):
                messagebox.showinfo("Fin del juego", "¡Empate!")
                reiniciar_juego()

# Función para reiniciar el juego
def reiniciar_juego():
    global tablero
    tablero = [' ' for _ in range(9)]
    for boton in botones:
        boton.config(text=' ', state=tk.NORMAL)
    # Elegir aleatoriamente quién comienza
    if random.choice([True, False]):
        movimiento = movimiento_ia(tablero)
        tablero[movimiento] = JUGADOR_IA
        botones[movimiento].config(text=JUGADOR_IA, state=tk.DISABLED)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Tres en Raya")

# Crear los botones del tablero
botones = []
for i in range(9):
    boton = tk.Button(ventana, text=' ', font=('Arial', 20), width=5, height=2,
                      command=lambda i=i: clic_jugador(i))
    boton.grid(row=i // 3, column=i % 3)
    botones.append(boton)

# Botón para reiniciar el juego
boton_reiniciar = tk.Button(ventana, text="Reiniciar", font=('Arial', 12), command=reiniciar_juego)
boton_reiniciar.grid(row=3, column=0, columnspan=3, sticky="we")

# Iniciar el juego con un jugador aleatorio
reiniciar_juego()

# Iniciar el bucle principal de la ventana
ventana.mainloop()