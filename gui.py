import re
import threading
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mplcursors

from sweep import sweep


# ============================================================
# Validación para números tipo:
# 1, -1, 0.1, -0.1, 1e-3, 2.5E-6
# ============================================================

def validar_numero(texto):
    if texto == "":
        return True

    # Permite escribir valores parciales mientras tecleas:
    # ".", "-", "+", "0.", "-0.", "1e", "1e-", etc.
    if texto in [".", "-", "+", "-.", "+."]:
        return True

    try:
        float(texto)
        return True
    except ValueError:
        return False

def window_creation(recursos):
    window = tk.Tk()
    window.title("Keithley SMU Analyzer")
    window.geometry("1350x850")
    window.minsize(1200, 750)

    vcmd = window.register(validar_numero)

    cursores = []

    # ============================================================
    # Layout principal
    # ============================================================

    frame_config = ttk.LabelFrame(window, text="Configuración de barrido")
    frame_config.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

    frame_graficas = ttk.Frame(window)
    frame_graficas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    window.columnconfigure(0, weight=0)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)

    # ============================================================
    # Variables
    # ============================================================

    smu_stepper_var = tk.StringVar()
    smu_sweeper_var = tk.StringVar()

    puntos_var = tk.StringVar(value="11")
    nplc_var = tk.StringVar(value="1")
    delay_var = tk.StringVar(value="0.1")

    stepper_points_var = tk.StringVar(value="3")
    stepper_start_var = tk.StringVar(value="0")
    stepper_end_var = tk.StringVar(value="5")
    stepper_current_limit_var = tk.StringVar(value="0.01")

    sweeper_start_var = tk.StringVar(value="0")
    sweeper_end_var = tk.StringVar(value="5")
    sweeper_current_limit_var = tk.StringVar(value="0.01")

    status_var = tk.StringVar(value="Listo.")

    # ============================================================
    # Funciones auxiliares GUI
    # ============================================================

    def crear_entry(parent, label, variable, row):
        ttk.Label(parent, text=label).grid(
            row=row,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        entry = ttk.Entry(
            parent,
            textvariable=variable,
            validate="key",
            validatecommand=(vcmd, "%P"),
            width=20
        )

        entry.grid(
            row=row,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        return entry

    def limpiar_cursores():
        for cursor in cursores:
            try:
                cursor.remove()
            except Exception:
                pass

        cursores.clear()

    def leer_configuracion():
        smu_stepper = smu_stepper_var.get()
        smu_sweeper = smu_sweeper_var.get()

        if not recursos:
            raise ValueError("No hay recursos VISA conectados.")

        if smu_stepper in ["", "Selecciona un SMU", "No hay recursos conectados"]:
            raise ValueError("Selecciona el SMU stepper.")

        if smu_sweeper in ["", "Selecciona un SMU", "No hay recursos conectados"]:
            raise ValueError("Selecciona el SMU sweeper.")

        if smu_stepper == smu_sweeper:
            raise ValueError("El stepper y el sweeper no pueden ser el mismo recurso.")

        puntos = int(float(puntos_var.get()))
        nplc = float(nplc_var.get())
        delay = float(delay_var.get())

        stepper_points = int(float(stepper_points_var.get()))
        v_step_ini = float(stepper_start_var.get())
        v_step_fin = float(stepper_end_var.get())
        i_lim_step = float(stepper_current_limit_var.get())

        v_sweep_ini = float(sweeper_start_var.get())
        v_sweep_fin = float(sweeper_end_var.get())
        i_lim_sweep = float(sweeper_current_limit_var.get())

        if puntos < 2:
            raise ValueError("El número de puntos del sweeper debe ser mayor o igual a 2.")

        if stepper_points < 1:
            raise ValueError("El número de puntos del stepper debe ser mayor o igual a 1.")

        if nplc <= 0:
            raise ValueError("NPLC debe ser mayor que cero.")

        if delay < 0:
            raise ValueError("El delay no puede ser negativo.")

        if i_lim_step <= 0:
            raise ValueError("El límite de corriente del stepper debe ser mayor que cero.")

        if i_lim_sweep <= 0:
            raise ValueError("El límite de corriente del sweeper debe ser mayor que cero.")

        # Estas listas deben coincidir con lo que espera sweep.py
        Common_data_config = [
            puntos,
            nplc,
            delay
        ]

        stepper_data_config = [
            smu_stepper,
            stepper_points,
            v_step_ini,
            v_step_fin,
            i_lim_step
        ]

        sweeper_data_config = [
            smu_sweeper,
            v_sweep_ini,
            v_sweep_fin,
            i_lim_sweep
        ]

        return Common_data_config, stepper_data_config, sweeper_data_config

    # ============================================================
    # Frames de configuración
    # ============================================================

    frame_common = ttk.LabelFrame(frame_config, text="Parámetros generales")
    frame_common.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    crear_entry(frame_common, "Número de puntos sweeper", puntos_var, 0)
    crear_entry(frame_common, "NPLC", nplc_var, 1)
    crear_entry(frame_common, "Source-measure delay [s]", delay_var, 2)

    frame_stepper = ttk.LabelFrame(frame_config, text="SMU Stepper")
    frame_stepper.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    ttk.Label(frame_stepper, text="Recurso VISA").grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky="w"
    )

    menu_stepper = ttk.Combobox(
        frame_stepper,
        textvariable=smu_stepper_var,
        values=recursos if recursos else ["No hay recursos conectados"],
        state="readonly",
        width=35
    )
    menu_stepper.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    crear_entry(frame_stepper, "Puntos stepper", stepper_points_var, 1)
    crear_entry(frame_stepper, "Inicio stepper [V]", stepper_start_var, 2)
    crear_entry(frame_stepper, "Final stepper [V]", stepper_end_var, 3)
    crear_entry(frame_stepper, "Límite corriente stepper [A]", stepper_current_limit_var, 4)

    frame_sweeper = ttk.LabelFrame(frame_config, text="SMU Sweeper")
    frame_sweeper.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    ttk.Label(frame_sweeper, text="Recurso VISA").grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky="w"
    )

    menu_sweeper = ttk.Combobox(
        frame_sweeper,
        textvariable=smu_sweeper_var,
        values=recursos if recursos else ["No hay recursos conectados"],
        state="readonly",
        width=35
    )
    menu_sweeper.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    crear_entry(frame_sweeper, "Inicio sweeper [V]", sweeper_start_var, 1)
    crear_entry(frame_sweeper, "Final sweeper [V]", sweeper_end_var, 2)
    crear_entry(frame_sweeper, "Límite corriente sweeper [A]", sweeper_current_limit_var, 3)

    frame_control = ttk.LabelFrame(frame_config, text="Control")
    frame_control.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    label_status = ttk.Label(
        frame_control,
        textvariable=status_var,
        wraplength=350
    )
    label_status.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="w")

    if recursos:
        smu_stepper_var.set("Selecciona un SMU")
        smu_sweeper_var.set("Selecciona un SMU")
    else:
        smu_stepper_var.set("No hay recursos conectados")
        smu_sweeper_var.set("No hay recursos conectados")

    # ============================================================
    # Gráfica de salida
    # ============================================================

    frame_grafica_salida = ttk.LabelFrame(
        frame_graficas,
        text="Curvas de salida"
    )
    frame_grafica_salida.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    fig_salida = Figure(figsize=(7, 4), dpi=100)
    ax_salida = fig_salida.add_subplot(111)
    ax_salida.set_title("Curvas de salida")
    ax_salida.set_xlabel("VDS / VSWEEP [V]")
    ax_salida.set_ylabel("IDS / ISWEEP [A]")
    ax_salida.grid(True)

    canvas_salida = FigureCanvasTkAgg(fig_salida, master=frame_grafica_salida)
    canvas_salida.draw()
    canvas_salida.get_tk_widget().pack(fill="both", expand=True)

    # ============================================================
    # Gráfica de entrada / transferencia
    # ============================================================

    frame_grafica_entrada = ttk.LabelFrame(
        frame_graficas,
        text="Curva de transferencia"
    )
    frame_grafica_entrada.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    fig_entrada = Figure(figsize=(7, 4), dpi=100)
    ax_entrada = fig_entrada.add_subplot(111)
    ax_entrada.set_title("Curva de transferencia")
    ax_entrada.set_xlabel("VGS / VSTEP [V]")
    ax_entrada.set_ylabel("IDS / ISWEEP [A]")
    ax_entrada.grid(True)

    canvas_entrada = FigureCanvasTkAgg(fig_entrada, master=frame_grafica_entrada)
    canvas_entrada.draw()
    canvas_entrada.get_tk_widget().pack(fill="both", expand=True)

    frame_graficas.rowconfigure(0, weight=1)
    frame_graficas.rowconfigure(1, weight=1)
    frame_graficas.columnconfigure(0, weight=1)

    # ============================================================
    # Actualización de gráficas
    # ============================================================

    def actualizar_graficas(data_salida):
        limpiar_cursores()

        if not data_salida:
            raise ValueError("El barrido no regresó datos.")

        grupos = defaultdict(list)

        for fila in data_salida:
            vstep = fila["VSTEP_set"]
            grupos[vstep].append(fila)

        # -----------------------------
        # Curvas de salida: IDS vs VDS
        # Una curva por cada VSTEP
        # -----------------------------

        ax_salida.clear()
        ax_salida.set_title("Curvas de salida")
        ax_salida.set_xlabel("VDS / VSWEEP [V]")
        ax_salida.set_ylabel("IDS / ISWEEP [A]")
        ax_salida.grid(True)

        lineas_salida = []

        for vstep in sorted(grupos.keys()):
            curva = grupos[vstep]

            x_salida = [
                fila.get("VSWEEP_meas", fila["VSWEEP_set"])
                for fila in curva
            ]

            y_salida = [
                fila["ISWEEP_meas"]
                for fila in curva
            ]

            linea, = ax_salida.plot(
                x_salida,
                y_salida,
                marker="o",
                label=f"VSTEP = {vstep:.4g} V"
            )

            lineas_salida.append(linea)

        ax_salida.legend()
        canvas_salida.draw()

        # -----------------------------
        # Curva de transferencia:
        # IDS vs VSTEP tomando el último punto del sweeper
        # -----------------------------

        ax_entrada.clear()
        ax_entrada.set_title("Curva de transferencia")
        ax_entrada.set_xlabel("VGS / VSTEP [V]")
        ax_entrada.set_ylabel("IDS / ISWEEP [A]")
        ax_entrada.grid(True)

        x_entrada = []
        y_entrada = []

        for vstep in sorted(grupos.keys()):
            curva = grupos[vstep]
            ultimo_punto = curva[-1]

            x_entrada.append(
                ultimo_punto.get("VSTEP_meas", ultimo_punto["VSTEP_set"])
            )

            y_entrada.append(
                ultimo_punto["ISWEEP_meas"]
            )

        linea_entrada, = ax_entrada.plot(
            x_entrada,
            y_entrada,
            marker="o"
        )

        canvas_entrada.draw()

        if lineas_salida:
            cursores.append(mplcursors.cursor(lineas_salida, hover=False))

        cursores.append(mplcursors.cursor(linea_entrada, hover=False))

    # ============================================================
    # Ejecución del barrido
    # ============================================================

    def finalizar_barrido(data_salida=None, error=None):
        boton_go.config(state="normal")

        if error is not None:
            status_var.set("Error en el barrido.")
            messagebox.showerror("Error", error)
            return

        try:
            actualizar_graficas(data_salida)
            status_var.set("Barrido terminado correctamente.")
        except Exception as e:
            status_var.set("Error al graficar los datos.")
            messagebox.showerror(
                "Error al graficar",
                f"{e}\n\n{traceback.format_exc()}"
            )

    def ejecutar_barrido():
        try:
            Common_data_config, stepper_data_config, sweeper_data_config = leer_configuracion()
        except Exception as e:
            messagebox.showerror("Configuración inválida", str(e))
            return

        boton_go.config(state="disabled")
        status_var.set("Ejecutando barrido...")

        print("\n==============================")
        print("Configuración enviada a sweep()")
        print("==============================")
        print("Common:", Common_data_config)
        print("Stepper:", stepper_data_config)
        print("Sweeper:", sweeper_data_config)

        def tarea():
            try:
                data_salida = sweep(
                    Common_data_config,
                    stepper_data_config,
                    sweeper_data_config
                )

                window.after(
                    0,
                    lambda: finalizar_barrido(data_salida=data_salida)
                )

            except Exception as e:
                error = f"{e}\n\n{traceback.format_exc()}"

                window.after(
                    0,
                    lambda: finalizar_barrido(error=error)
                )

        hilo = threading.Thread(target=tarea, daemon=True)
        hilo.start()

    boton_go = ttk.Button(
        frame_control,
        text="Go",
        command=ejecutar_barrido
    )
    boton_go.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    boton_salir = ttk.Button(
        frame_control,
        text="Salir",
        command=window.destroy
    )
    boton_salir.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    frame_control.columnconfigure(0, weight=1)
    frame_control.columnconfigure(1, weight=1)

    return window