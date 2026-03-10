import time
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

try:
    import pyvisa
except ImportError:
    print("No se encontró pyvisa. Instala con:")
    print("pip install pyvisa matplotlib numpy")
    sys.exit(1)


# =========================
# CONFIGURACION DEL BARRIDO
# =========================
START_V = 0.0        # Voltaje inicial
STOP_V = 5.0         # Voltaje final
POINTS = 21          # Numero de puntos
CURRENT_LIMIT = 0.01 # Limite de corriente en A (10 mA)
DELAY_S = 0.2        # Tiempo de espera entre punto y medicion
CSV_NAME = "barrido_keithley.csv"

# Si ya conoces el recurso VISA, ponlo aqui:
# por ejemplo "GPIB0::24::INSTR" o "ASRL3::INSTR" o "USB0::0x05E6::..."
RESOURCE_NAME = None


def listar_recursos(rm):
    recursos = rm.list_resources()
    print("Recursos VISA detectados:")
    if not recursos:
        print("  No se detectaron recursos.")
    else:
        for i, r in enumerate(recursos, 1):
            print(f"  {i}. {r}")
    return recursos


def seleccionar_recurso(rm):
    recursos = listar_recursos(rm)
    if not recursos:
        raise RuntimeError("No hay recursos VISA disponibles.")
    idx = int(input("Selecciona el numero del recurso: "))
    return recursos[idx - 1]


def abrir_instrumento(rm, resource_name):
    inst = rm.open_resource(resource_name)
    inst.timeout = 10000
    inst.write_termination = "\n"
    inst.read_termination = "\n"
    return inst


def configurar_2400(inst, current_limit):
    """
    Configuracion tipo Keithley 2400:
    Fuente de voltaje, medicion de corriente.
    """
    inst.write("*RST")
    inst.write("*CLS")
    inst.write(":SYST:RSEN OFF")                # 2 hilos
    inst.write(':SOUR:FUNC VOLT')
    inst.write(':SOUR:VOLT:MODE FIX')
    inst.write(':SENS:FUNC "CURR"')
    inst.write(f':SENS:CURR:PROT {current_limit}')
    inst.write(':SENS:CURR:RANG:AUTO ON')
    inst.write(':FORM:ELEM VOLT,CURR')
    inst.write(':OUTP ON')


def configurar_2450_fallback(inst, current_limit):
    """
    Intento alterno para 2450 si el bloque 2400 no funciona.
    """
    inst.write("*RST")
    inst.write("*CLS")
    inst.write(':SOUR:FUNC VOLT')
    inst.write(':SOUR:VOLT:ILIM ' + str(current_limit))
    inst.write(':SENS:FUNC "CURR"')
    inst.write(':FORM:ELEM VOLT,CURR')
    inst.write(':OUTP ON')


def parsear_respuesta(raw, v_programado=None):
    """
    Espera algo como:
    '0.100000E+00,0.999000E-04'
    o mas elementos separados por coma.
    """
    vals = [x.strip() for x in raw.strip().split(",") if x.strip() != ""]
    nums = [float(x) for x in vals]

    if len(nums) >= 2:
        return nums[0], nums[1]
    elif len(nums) == 1:
        # Si solo regresa corriente, usamos el voltaje programado como respaldo
        return v_programado, nums[0]
    else:
        raise ValueError(f"No se pudo interpretar la respuesta: {raw}")


def barrer_voltaje(inst, start_v, stop_v, points, delay_s):
    v_set = np.linspace(start_v, stop_v, points)
    v_meas = []
    i_meas = []

    print("\nIniciando barrido...\n")
    for k, v in enumerate(v_set, 1):
        inst.write(f":SOUR:VOLT {v}")
        time.sleep(delay_s)

        try:
            raw = inst.query(":READ?")
            vm, im = parsear_respuesta(raw, v_programado=v)
        except Exception:
            # Fallback simple
            try:
                raw_i = inst.query(":MEAS:CURR?")
                vm, im = parsear_respuesta(raw_i, v_programado=v)
            except Exception as e:
                print(f"Error en punto {k}: {e}")
                vm, im = v, np.nan

        v_meas.append(vm)
        i_meas.append(im)

        print(
            f"Punto {k:02d}/{points} | "
            f"V_prog = {v:8.4f} V | "
            f"V_med = {vm:8.4f} V | "
            f"I_med = {im: .6e} A"
        )

    return np.array(v_set), np.array(v_meas), np.array(i_meas)


def guardar_csv(filename, v_set, v_meas, i_meas):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["V_programado_V", "V_medido_V", "I_medida_A"])
        for a, b, c in zip(v_set, v_meas, i_meas):
            writer.writerow([a, b, c])
    print(f"\nDatos guardados en: {filename}")


def graficar(v_set, v_meas, i_meas):
    plt.figure()
    plt.plot(v_set, v_meas, marker="o")
    plt.xlabel("Voltaje programado (V)")
    plt.ylabel("Voltaje medido (V)")
    plt.title("Voltaje programado vs voltaje medido")
    plt.grid(True)

    plt.figure()
    plt.plot(v_meas, i_meas, marker="o")
    plt.xlabel("Voltaje medido (V)")
    plt.ylabel("Corriente medida (A)")
    plt.title("Curva I-V")
    plt.grid(True)

    plt.show()


def apagar_salida(inst):
    try:
        inst.write(":SOUR:VOLT 0")
    except Exception:
        pass
    try:
        inst.write(":OUTP OFF")
    except Exception:
        pass


def main():
    rm = pyvisa.ResourceManager()

    try:
        resource = RESOURCE_NAME if RESOURCE_NAME else seleccionar_recurso(rm)
        print(f"\nAbriendo: {resource}")
        inst = abrir_instrumento(rm, resource)

        try:
            print("IDN:", inst.query("*IDN?").strip())
        except Exception as e:
            print("No se pudo leer *IDN?:", e)

        # Primero intenta configuracion estilo 2400
        try:
            configurar_2400(inst, CURRENT_LIMIT)
            print("Configuracion tipo 2400 aplicada.")
        except Exception as e:
            print("Fallo configuracion 2400, intentando 2450:", e)
            configurar_2450_fallback(inst, CURRENT_LIMIT)
            print("Configuracion alterna tipo 2450 aplicada.")

        v_set, v_meas, i_meas = barrer_voltaje(
            inst,
            START_V,
            STOP_V,
            POINTS,
            DELAY_S
        )

        guardar_csv(CSV_NAME, v_set, v_meas, i_meas)
        graficar(v_set, v_meas, i_meas)

    except Exception as e:
        print("Error general:", e)

    finally:
        try:
            apagar_salida(inst)
            inst.close()
            print("Instrumento cerrado.")
        except Exception:
            pass
        try:
            rm.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()