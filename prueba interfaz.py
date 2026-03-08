#importamos libreria thinter
import tkinter as tk

from tkinter import ttk
def selSMUstepper():
    whSMU = selection_SMU.get().strip()

    if whSMU not in ("2400","2450"):
        resultado.config(text="Elija un SMU configurable")
    else:
        resultado.config(text=f"SMU seleccionado como stepper: {whSMU}")
    
    
###Ventana principal
window = tk.Tk()
window.title("Keithley")
window.geometry("1800x920")

#Etiqueta de instruccion
etiquetawhSMU = tk.Label(window, text="¿Que SMU sera tu stepper?")
etiquetawhSMU.pack(pady=10)

selection_SMU=tk.StringVar()

#combobox de seleccion de SMU
menu_step=ttk.Combobox(
    window,
    textvariable = selection_SMU,
    values = ["2400","2450"],
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

