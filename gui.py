import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mplcursors
from sweep import barrer_voltaje


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
    ########### GRAFICAS ###########
    frame_grafica_curvas_entrada=tk.LabelFrame(window, text="Curvas de entrada",width=550,height=400)
    frame_grafica_curvas_entrada.place(x=800,y=420)

    frame_grafica_curvas_salida=tk.LabelFrame(window, text="Curvas de salida",width=550,height=400)
    frame_grafica_curvas_salida.place(x=800,y=20)
    ##############LABEL GRAFICAS#############
    label_entrada=tk.Label(window,text="Seleccione un punto para ver sus valores",anchor="w")
    label_entrada.place(x=800,y=0)
    ##############Figuras Graficas########
    fig_salida=Figure(figsize=(5, 3.8), dpi=100)
    ax_salida= fig_salida.add_subplot(111)
    ax_salida.set_title("Curvas de salida")
    ax_salida.set_xlabel("VDS")
    ax_salida.set_ylabel("IDS")
    ax_salida.grid(True)

    fig_entrada=Figure(figsize=(5, 3.8), dpi=100)
    ax_entrada= fig_entrada.add_subplot(111)
    ax_entrada.set_title("Curvas de transferencia / Transconductuales")
    ax_entrada.set_xlabel("VGS")
    ax_entrada.set_ylabel("IGS")
    ax_entrada.grid(True)
    ################Canvas salida################
    canvas_salida=FigureCanvasTkAgg(fig_salida, master=frame_grafica_curvas_salida)
    canvas_salida.draw()
    canvas_salida.get_tk_widget().pack(fill="both",expand=True)

    canvas_entrada=FigureCanvasTkAgg(fig_entrada,master=frame_grafica_curvas_entrada)
    canvas_entrada.draw()
    canvas_entrada.get_tk_widget().pack(fill="both",expand=True)
    ######Datos a graficar######
        #Salida


        #Entrada


    # Resultado
    #resultado = ttk.Label(window, text="")
    #resultado.place(x=10, y=250)

    # Botón
    def ejecutar_barrido():
        smu_stepper = menu_stepper.get()
        smu_sweeper = menu_sweeper.get()

        puntos = entrynp.get()
        nplc = NLPC.get()
        delay = SourceMeasureDelay.get()

        step_points = stepper_points.get()
        v_step_ini = stepper_Start.get()
        v_step_fin = stepper_end.get()
        i_lim_step = stepper_current_limit.get()

        v_sweep_ini = sweeper_start.get()
        v_sweep_fin = sweeper_end.get()
        i_lim_sweep = sweeper_current_limit.get()

        Comon_data_config=[puntos,nplc,delay]
        stepper_data_config=[smu_stepper,step_points,v_step_ini,v_step_fin,i_lim_step]
        sweeper_data_config=[smu_sweeper,v_sweep_ini,v_sweep_fin,i_lim_sweep]

        print("Stepper:", smu_stepper)
        print("Sweeper:", smu_sweeper)
        print("Puntos:", puntos)

        # aquí mandas llamar tu función real de barrido
        # x_salida, y_salida, x_entrada, y_entrada = funcion_barrido(...)

        # ejemplo de prueba
        data_salida=sweep(Comon_data_config,stepper_data_config,sweeper_data_config)
        

        # actualizar gráficas
        ax_salida.clear()
        ax_salida.set_title("Curvas de salida")
        ax_salida.set_xlabel("VDS")
        ax_salida.set_ylabel("IDS")
        ax_salida.grid(True)
        linea_salida, = ax_salida.plot(x_salida, y_salida, marker="o")
        canvas_salida.draw()

        ax_entrada.clear()
        ax_entrada.set_title("Curvas de transferencia / Transconductuales")
        ax_entrada.set_xlabel("VGS")
        ax_entrada.set_ylabel("IGS")
        ax_entrada.grid(True)
        linea_entrada, = ax_entrada.plot(x_entrada, y_entrada, marker="o")
        canvas_entrada.draw()

        # cursores interactivos
        mplcursors.cursor(linea_salida, hover=False)
        mplcursors.cursor(linea_entrada, hover=False)

    boton_go = ttk.Button(window, text="Go", command=ejecutar_barrido)
    boton_go.place(x=400, y=320)

    return window