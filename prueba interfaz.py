#importamos libreria thinter
import tkinter as tk
def selstepper():
    whsmu = entrada.get().strip()  #Lee lo que esta escrito en la caja
    if whsmu == "":
        resultado.config(text=f"Porfavor escriba un SMU correcto")
    elif whsmu not in ("2450","2400"):
        resultado.config(text=f"Porfavor escriba un SMU correcto (2450 o 2400)")        
    else:
        resultado.config(text=f"SMU seleccionado: {whsmu}")
    
###Ventana principal
window = tk.Tk()
window.title("Keithley")
window.geometry("1800x920")

#Etiqueta de instruccion
etiquetawhSMU = tk.Label(window, text="¿Que SMU sera tu stepper?")
etiquetawhSMU.pack(pady=10)

#Caja de texto
entrada = tk.Entry(window, width=30)
entrada.pack(pady=30)

#Boton de seleccion de SMU
SelecSMU = tk.Button(window, text="SMU", command=selstepper)
SelecSMU.pack(pady=50)

resultado = tk.Label(window, text="")
resultado.pack(pady=60)

#Mantener ventana abierta
window.mainloop()

