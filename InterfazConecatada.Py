import time
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import pyvisa
import tkinter as tk
from tkinter import tkk

def listar_recursos(rm):
    recursos = rm.list_resources()
    print("Recursos VISA detectados:")
    if not recursos:
        print("  No se detectaron recursos.")
    else:
        for i, r in enumerate(recursos, 1):
            print(f"  {i}. {r}")
    return recursos

###Ventana principal
window = tk.Tk()
window.title("Keithley")
window.geometry("1800x920")

#Etiqueta de instruccion
etiquetawhSMU = tk.Label(window, text="¿Que SMU sera tu stepper?")
etiquetawhSMU.pack(pady=10)

selection_SMU=tk.StringVar()

#combobox de seleccion de SMU
    if not recursos:
        menu_step=ttk.Combobox(
        window,
        textvariable = selection_SMU,
        values = ["No hay recursos conectados"],
        state = "readonly",
        width=20
        )
        menu_step.pack(pady=20)
        menu_step.set("Selecciona un SMU")
    else 
        menu_step=ttk.Combobox(
        window,
        textvariable = selection_SMU,
        values = [{i},{r}],
        state = "readonly",
        width=20
        )
        menu_step.pack(pady=20)
        menu_step.set("Selecciona un SMU")

#Boton
boton_step=tk.Button(window,text="Seleccionar SMU stepper", command=selSMUstepper)
boton_step.pack(pady=30)


resultado = tk.Label(window, text="")
resultado.pack(pady=60)

#Mantener ventana abierta
window.mainloop()
