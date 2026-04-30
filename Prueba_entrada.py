import tkinter as tk
from tkinter import ttk

def validar_numero(texto):
    if texto == "":
        return True
    return texto.isdigit()

def mostrar_valor():
    valor = entrada.get()
    resultado.config(text=f"Valor: {valor}")

def crear_ventana():
    global entrada, resultado

    window = tk.Tk()
    window.title("Keithley")
    window.geometry("400x250")

    vcmd = window.register(validar_numero)

    ttk.Label(window, text="Ingresa un número:").pack(pady=10)

    entrada = ttk.Entry(window, validate="key", validatecommand=(vcmd, "%P"))
    entrada.pack(pady=10)

    ttk.Button(window, text="Aceptar", command=mostrar_valor).pack(pady=10)

    resultado = ttk.Label(window, text="")
    resultado.pack(pady=10)

    return window

def main():
    window = crear_ventana()
    window.mainloop()

if __name__ == "__main__":
    main()
    