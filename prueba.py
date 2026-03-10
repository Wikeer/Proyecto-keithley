import argparse
import sys

try:
    import pyvisa
except ImportError:
    print("Error: no se encontró pyvisa.")
    print("Instálalo con: pip install pyvisa")
    sys.exit(1)


def printable(text):
    """Muestra caracteres especiales de forma visible."""
    return repr(text)[1:-1]


def open_resource(rm, resource_name, baudrate, timeout_ms, read_term, write_term):
    inst = rm.open_resource(resource_name)

    # Configuración básica
    inst.timeout = timeout_ms
    inst.read_termination = read_term
    inst.write_termination = write_term

    # Si es recurso serial, intentamos configurar baudrate
    if resource_name.upper().startswith("ASRL"):
        try:
            inst.baud_rate = baudrate
        except Exception as e:
            print(f"Aviso: no se pudo configurar baudrate: {e}")

    return inst


def try_query_idn(inst):
    print("\nProbando comunicación con *IDN? ...")
    try:
        response = inst.query("*IDN?")
        print(f"Respuesta: {response.strip()}")
        return True
    except Exception as e:
        print(f"No se pudo leer *IDN?: {e}")
        return False


def interactive_console(inst):
    print("\nConsola interactiva SCPI")
    print("Escribe comandos SCPI para enviarlos al instrumento.")
    print("Comandos especiales:")
    print("  idn   -> envía *IDN?")
    print("  cls   -> envía *CLS")
    print("  rst   -> envía *RST")
    print("  read  -> intenta leer manualmente")
    print("  exit  -> salir")
    print()

    while True:
        try:
            cmd = input("SCPI> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if not cmd:
            continue

        low = cmd.lower()

        if low in ("exit", "quit", "salir"):
            print("Saliendo...")
            break

        elif low == "idn":
            try:
                print(inst.query("*IDN?").strip())
            except Exception as e:
                print(f"Error: {e}")

        elif low == "cls":
            try:
                inst.write("*CLS")
                print("OK: *CLS enviado")
            except Exception as e:
                print(f"Error: {e}")

        elif low == "rst":
            try:
                inst.write("*RST")
                print("OK: *RST enviado")
            except Exception as e:
                print(f"Error: {e}")

        elif low == "read":
            try:
                response = inst.read()
                print(f"RX: {response}")
            except Exception as e:
                print(f"Error al leer: {e}")

        else:
            try:
                # Si parece consulta, usamos query para escribir y leer
                if cmd.endswith("?"):
                    response = inst.query(cmd)
                    print(f"RX: {response.strip()}")
                else:
                    inst.write(cmd)
                    print("TX OK")
            except Exception as e:
                print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Prueba de conexión e ingreso manual de comandos SCPI para Keithley"
    )
    parser.add_argument(
        "--resource",
        help='Recurso VISA específico, por ejemplo "GPIB0::24::INSTR" o "ASRL3::INSTR"',
        default=None
    )
    parser.add_argument(
        "--baudrate",
        type=int,
        default=9600,
        help="Baudrate para puertos seriales ASRL (default: 9600)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5000,
        help="Timeout en milisegundos (default: 5000)"
    )
    parser.add_argument(
        "--read-term",
        default="\n",
        help=r'Terminación de lectura, por ejemplo "\n"'
    )
    parser.add_argument(
        "--write-term",
        default="\n",
        help=r'Terminación de escritura, por ejemplo "\n"'
    )

    args = parser.parse_args()

    print("=== Prueba de conexión Keithley / VISA ===")
    print(f"read_termination = {printable(args.read_term)}")
    print(f"write_termination = {printable(args.write_term)}")
    print(f"timeout = {args.timeout} ms")
    print()

    try:
        rm = pyvisa.ResourceManager()
    except Exception as e:
        print(f"No se pudo abrir ResourceManager: {e}")
        sys.exit(1)

    try:
        resources = rm.list_resources()
        print("Recursos VISA detectados:")
        if resources:
            for i, r in enumerate(resources, start=1):
                print(f"  {i}. {r}")
        else:
            print("  No se detectaron recursos VISA.")
    except Exception as e:
        print(f"No se pudieron listar recursos: {e}")
        resources = ()

    resource_name = args.resource

    if not resource_name:
        if not resources:
            print("\nNo hay recursos disponibles y no se indicó --resource.")
            sys.exit(1)

        print("\nSelecciona el número del recurso a abrir.")
        try:
            idx = int(input("Número: ").strip())
            resource_name = resources[idx - 1]
        except Exception:
            print("Selección inválida.")
            sys.exit(1)

    print(f"\nAbriendo recurso: {resource_name}")

    inst = None
    try:
        inst = open_resource(
            rm=rm,
            resource_name=resource_name,
            baudrate=args.baudrate,
            timeout_ms=args.timeout,
            read_term=args.read_term,
            write_term=args.write_term,
        )
        print("Conexión abierta correctamente.")
        try_query_idn(inst)
        interactive_console(inst)

    except Exception as e:
        print(f"Error al abrir o usar el recurso: {e}")

    finally:
        if inst is not None:
            try:
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