import time
import csv
import sys
import numpy as np  

def sweep(Comon_data_config,stepper_data_config,sweeper_data_config):
    
    stepper=stepper_data_config[1][0]
    sweeper=sweeper_data_config[1][0]
    current_limit=stepper_data_config[5][0]
    ############## INICIALIZACION INTRUMENTO

    def config_stepper(stepper):
        stepper.write("*RST")
        stepper.write("*CLS")
        stepper.write(':SYST:RSEN OFF')
        stepper.write(':SOUR:FUNC VOLT')
        stepper.write(':SOUR:VOLT:MODE FIX')
        stepper.write(':SENS:FUNC "CURR"')
        stepper.write(f':SENS:CURR:PROT {current_limit}')

        

