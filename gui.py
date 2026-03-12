import tkinter as tk
from tkinter import ttk

def window_creation(recursos):
    window = tk.Tk()
    window.title("Keithley")
    window.geometry("600x400")

    menu = ttk.Combobox(
        window,
        values=recursos if recursos else ["No hay recursos conectados"],
        state="readonly",
        width=40
    )
    menu.pack(pady=60,padx=60)
    menu.place(x=0,y=0)
    if recursos:
        menu.set("Selecciona un SMU")
    else:
        menu.set("No hay recursos conectados")

    return window