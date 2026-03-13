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

    # Labels commons 
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

    title_stepper_sweep_start = tk.Label(window,text="Inicio stepper")
    title_stepper_sweep_start.place(x=10,y=360)

    title_stepper_sweep_end = tk.Label(window,text="Final stepper")
    title_stepper_sweep_end.place(x=10,y=430)

    title_current_limit_stepper=tk.Label(window,text="Limite de corriente stepper")
    title_current_limit_stepper.place(x=10,y=500)

    title_sweeper_start=tk.Label(window,text="Inicio barrido")
    title_sweeper_start.place(x=400,y=80)

    title_stepper = tk.Label(window, text="SMU Sweeper")
    title_stepper.place(x=400, y=10)

    title_sweeper_end=tk.Label(window,text="Final barrido")
    title_sweeper_end.place(x=400,y=150)

    title_current_limit_sweeper=tk.Label(window,text="Limite de corriente sweeper")
    title_current_limit_sweeper.place(x=400,y=220)
    # Combobox Stepper
    menu_stepper = ttk.Combobox(
        window,
        values=recursos if recursos else ["No hay recursos conectados"],
        state="readonly",
        width=40
    )
    menu_stepper.place(x=10, y=40)

    menu_sweeper = ttk.Combobox(
        window,
        values=recursos if recursos else ["No hay recursos conectados"],
        state="readonly",
        width=40
    )
    menu_sweeper.place(x=400, y=40)

    if recursos:
        menu_sweeper.set("Selecciona un SMU")
        menu_stepper.set("Selecciona un SMU")
    else:
        menu_stepper.set("No hay recursos conectados")
        menu_sweeper.set("No hay recursos conectados")

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

    #stepper sweep
    stepper_Start=ttk.Entry(window,validate="key",validatecommand=(vcmd,"%P"))
    stepper_Start.place(x=10,y=390)

    stepper_end=ttk.Entry(window,validate="key",validatecommand=(vcmd,"%P"))
    stepper_end.place(x=10,y=460)

    stepper_current_limit=ttk.Entry(window,validate="key",validatecommand=(vcmd,"%P"))
    stepper_current_limit.place(x=10,y=530)

    sweeper_start=ttk.Entry(window,validate="key",validatecommand=(vcmd,"%P"))
    sweeper_start.place(x=400,y=110)

    sweeper_end=ttk.Entry(window,validate="key",validatecommand=(vcmd, "%P"))
    sweeper_end.place(x=400,y=180)

    sweeper_current_limit=ttk.Entry(window,validate="key",validatecommand=(vcmd,"%P"))
    sweeper_current_limit.place(x=400,y=250)
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