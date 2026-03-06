import pyvisa

rm=pyvisa.ResourceManager('@ivi')

smu2400=rm.open_resource("GPIB0::22::INSTR")
smu2450=rm.open_resource("USB0::0x05E6::0x2450::04066511::INSTR")

print("2400:", smu2400.query("*IDN?"))
print("2450:", smu2450.query("*IDN?"))