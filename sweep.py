import time
import numpy as np
import pyvisa


def convertir_float(valor):
    """
    Permite escribir números como:
    0.01, 1e-3, 0,001
    """
    if isinstance(valor, str):
        valor = valor.replace(",", ".")
    return float(valor)


def convertir_int(valor):
    return int(convertir_float(valor))


def sweep(Common_data_config, stepper_data_config, sweeper_data_config):

    # ============================================================
    # Lectura de configuración desde la GUI
    # ============================================================

    sweeper_points = convertir_int(Common_data_config[0])
    nplc = convertir_float(Common_data_config[1])
    delay_s = convertir_float(Common_data_config[2])

    stepper_resource = stepper_data_config[0]
    stepper_points = convertir_int(stepper_data_config[1])
    v_stepper_ini = convertir_float(stepper_data_config[2])
    v_stepper_fin = convertir_float(stepper_data_config[3])
    current_limit_stepper = convertir_float(stepper_data_config[4])

    sweeper_resource = sweeper_data_config[0]
    v_sweeper_ini = convertir_float(sweeper_data_config[1])
    v_sweeper_fin = convertir_float(sweeper_data_config[2])
    current_limit_sweeper = convertir_float(sweeper_data_config[3])

    if sweeper_points < 2:
        raise ValueError("El número de puntos del sweeper debe ser mayor o igual a 2.")

    if stepper_points < 1:
        raise ValueError("El número de puntos del stepper debe ser mayor o igual a 1.")

    if current_limit_stepper <= 0:
        raise ValueError("El límite de corriente del stepper debe ser mayor que cero.")

    if current_limit_sweeper <= 0:
        raise ValueError("El límite de corriente del sweeper debe ser mayor que cero.")

    # ============================================================
    # Apertura de instrumentos
    # ============================================================

    rm = pyvisa.ResourceManager()

    stepper = rm.open_resource(stepper_resource)
    sweeper = rm.open_resource(sweeper_resource)

    for inst in [stepper, sweeper]:
        inst.timeout = 20000
        inst.write_termination = "\n"
        inst.read_termination = "\n"

    # ============================================================
    # Configuración de los SMU
    # ============================================================

    def config_smu(inst, current_limit):
        inst.write("*RST")
        time.sleep(0.5)
        inst.write("*CLS")

        inst.write(":SYST:RSEN OFF")
        inst.write(":SOUR:FUNC VOLT")
        inst.write(":SOUR:VOLT:MODE FIX")

        inst.write(':SENS:FUNC "CURR"')
        inst.write(f":SENS:CURR:PROT {current_limit}")
        inst.write(":SENS:CURR:RANG:AUTO ON")
        inst.write(f":SENS:CURR:NPLC {nplc}")

        inst.write(":FORM:ELEM VOLT,CURR")
        inst.write(":OUTP ON")

    def pars_ans(raw, v_programado=None):
        vals = [x.strip() for x in raw.strip().split(",") if x.strip() != ""]
        nums = [float(x) for x in vals]

        if len(nums) >= 2:
            return nums[0], nums[1]

        elif len(nums) == 1:
            return v_programado, nums[0]

        else:
            raise ValueError(f"No se pudo interpretar la respuesta: {raw}")

    def medir(inst, v_programado):
        try:
            raw = inst.query(":READ?")
            return pars_ans(raw, v_programado=v_programado)

        except Exception:
            raw = inst.query(":MEAS:CURR?")
            return pars_ans(raw, v_programado=v_programado)

    # ============================================================
    # Vectores de barrido
    # ============================================================

    v_stepper_set = np.linspace(
        v_stepper_ini,
        v_stepper_fin,
        stepper_points
    )

    v_sweeper_set = np.linspace(
        v_sweeper_ini,
        v_sweeper_fin,
        sweeper_points
    )

    data = []

    print("\nIniciando barrido correcto...")
    print(f"Puntos sweeper por curva: {sweeper_points}")
    print(f"Puntos stepper / curvas: {stepper_points}")
    print(f"Total de mediciones: {sweeper_points * stepper_points}")

    # ============================================================
    # Barrido correcto:
    #
    # Para cada VSTEP, se barre completo VSWEEP
    # ============================================================

    try:
        config_smu(stepper, current_limit_stepper)
        config_smu(sweeper, current_limit_sweeper)

        for k, v_step in enumerate(v_stepper_set, start=1):

            print("\n----------------------------------")
            print(f"Stepper {k}/{stepper_points}")
            print(f"VSTEP = {v_step:.6g} V")
            print("----------------------------------")

            stepper.write(f":SOUR:VOLT {v_step}")
            time.sleep(delay_s)

            for j, v_sweep in enumerate(v_sweeper_set, start=1):

                sweeper.write(f":SOUR:VOLT {v_sweep}")
                time.sleep(delay_s)

                v_sweep_meas, i_sweep_meas = medir(sweeper, v_sweep)
                v_step_meas, i_step_meas = medir(stepper, v_step)

                fila = {
                    "step_index": k,
                    "sweep_index": j,

                    "VSTEP_set": float(v_step),
                    "VSTEP_meas": float(v_step_meas),
                    "ISTEP_meas": float(i_step_meas),

                    "VSWEEP_set": float(v_sweep),
                    "VSWEEP_meas": float(v_sweep_meas),
                    "ISWEEP_meas": float(i_sweep_meas),
                }

                data.append(fila)

                print(
                    f"Punto {j}/{sweeper_points} | "
                    f"VSWEEP = {v_sweep_meas:.6e} V | "
                    f"ISWEEP = {i_sweep_meas:.6e} A"
                )

    finally:
        try:
            sweeper.write(":SOUR:VOLT 0")
            stepper.write(":SOUR:VOLT 0")

            sweeper.write(":OUTP OFF")
            stepper.write(":OUTP OFF")

        except Exception:
            pass

    print("\nBarrido terminado correctamente.")

    return data