import tkinter as tk
from tkinter import ttk

def mostrar():
    resultado.config(text=f"StringVar dice: {dato.get()}")

def escribir():
    dato.set("999")

window = tk.Tk()

dato = tk.StringVar()

entrada = ttk.Entry(window, textvariable=dato)
entrada.pack(pady=10)

ttk.Button(window, text="Leer StringVar", command=mostrar).pack(pady=5)
ttk.Button(window, text="Poner 999", command=escribir).pack(pady=5)

resultado = ttk.Label(window, text="")
resultado.pack(pady=10)

window.mainloop()