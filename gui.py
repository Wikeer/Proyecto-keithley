import tkinter as tk
from tkinter import ttk


def validar_numero(texto):
    if texto == "":
        return True
    return texto.isdigit()


def window_creation(recursos):
    window = tk.Tk()
    window.title("Keithley")
    window.geometry("600x400")

    vcmd = window.register(validar_numero)

    # Labels
    title_stepper = tk.Label(window, text="SMU stepper")
    title_stepper.place(x=10, y=10)

    title_points = tk.Label(window, text="Number of points")
    title_points.place(x=10, y=80)

    title_nplc = tk.Label(window, text="NPLC")
    title_nplc.place(x=10, y=150)

    title_sourcedelay=tk.Label(window, text="Source to measure delay")
    title_sourcedelay.place(x=10, y=220)

    title_stepper_points = tk.Label(window,text="Stepper points")
    title_stepper_points.place(x=10,y=290)

    # Combobox Stepper
    menu = ttk.Combobox(
        window,
        values=recursos if recursos else ["No hay recursos conectados"],
        state="readonly",
        width=40
    )
    menu.place(x=10, y=40)

    if recursos:
        menu.set("Selecciona un SMU")
    else:
        menu.set("No hay recursos conectados")

    # Entry Number of Points
    entrynp = ttk.Entry(window, validate="key", validatecommand=(vcmd, "%P"))
    entrynp.place(x=10, y=110)
    #Entry NPLC
    NLPC = ttk.Entry(window, validate="key", validatecommand=(vcmd, "%P"))
    NLPC.place(x=10, y=180)
    #Source to measure delay
    SourceMeasureDelay=ttk.Entry(window,validate="key",validatecommand=(vcmd, "%P"))
    SourceMeasureDelay.place(x=10, y=250)
    #Stepper points
    stepper_points=ttk.Entry(window,validate="key",validatecommand=(vcmd, "%P"))
    stepper_points.place(x=10,y=320)
    # Resultado
    #resultado = ttk.Label(window, text="")
    #resultado.place(x=10, y=250)

    # Botón
    #def mostrar_valor():
    #    valor = entrada.get()
    #    resultado.config(text=f"Valor: {valor}")

    #boton = ttk.Button(window, text="Mostrar valor", command=mostrar_valor)
    #boton.place(x=10, y=210)

    return window