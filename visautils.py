import pyvisa

def resource_list():
    rm=pyvisa.ResourceManager()
    resources=rm.list_resources()
    return resources 

