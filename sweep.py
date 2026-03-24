import time
import csv
import sys
import numpy as np  

def sweep(Comon_data_config,stepper_data_config,sweeper_data_config):
    
    stepper=stepper_data_config[1][0]
    sweeper=sweeper_data_config[1][0]
    current_limit_stepper=stepper_data_config[5][0]
    current_limit_sweeper=sweeper_data_config[4][0]
    ############## INICIALIZACION INTRUMENTO

    def config_stepper(stepper):
        stepper.write("*RST")
        stepper.write("*CLS")
        stepper.write(':SYST:RSEN OFF')
        stepper.write(':SOUR:FUNC VOLT')
        stepper.write(':SOUR:VOLT:MODE FIX')                # 2 Hilo
        stepper.write(':SENS:FUNC "CURR"')
        stepper.write(f':SENS:CURR:PROT {current_limit_stepper}')
        stepper.write('SENS:CUTT:RANG:AUTO ON')
        stepper.write(':FORM:ELEM VOLT,CURR')
        stepper.write(':OUTP ON')

    def config_sweeper(sweeper):
        sweeper.write("*RST")
        sweeper.write("*CLS")
        sweeper.write(':SYST:RSEN OFF')
        sweeper.write(':SOUR:FUNC VOLT')
        sweeper.write(':SOUR:VOLT:MODE FIX')                # 2 Hilo
        sweeper.write(':SENS:FUNC "CURR"')
        sweeper.write(f':SENS:CURR:PROT {current_limit_sweeper}')
        sweeper.write('SENS:CUTT:RANG:AUTO ON')
        sweeper.write(':FORM:ELEM VOLT,CURR')
        sweeper.write(':OUTP ON')
    
    def pars_ans(raw, v_programado=None):
        #"""
        #Espera algo como:
        #'0.100000E+00,0.999000E-04'
        #o mas elementos separados por coma.
        #"""
        vals = [x.strip() for x in raw.strip().split(",") if x.strip() != ""]
        nums = [float(x) for x in vals]

        if len(nums) >= 2:
            return nums[0], nums[1]
        elif len(nums) == 1:
            # Si solo regresa corriente, usamos el voltaje programado como respaldo
            return v_programado, nums[0]
        else:
            raise ValueError(f"No se pudo interpretar la respuesta: {raw}")


    def barrer_voltaje(Common_data_config,stepper_data_config,sweeper_data_config):
        v_stepper_ini=stepper_data_config[3][0]
        v_sweeper_ini=sweeper_data_config[2][0]
        v_stepper_fin=stepper_data_config[4][0]
        v_sweeper_fin=sweeper_data_config[3][0]
        stepper_points=stepper_data_config[2][0]
        points=Common_data_config[1][0]
        delay_s=Common_data_config[3][0]
        v_stepper_set=np.linspace(v_stepper_ini,v_stepper_fin,points)
        v_sweeper_set=np.linspace(v_sweeper_ini,v_sweeper_fin,points)
        vds_meas=[]
        ids_meas=[]
        vg_meas=[]

        print("\Iniciando barrido...")
        for k, SV in enumerate(v_stepper_set,1):
            stepper.write(f":SOUR:VOLT {SV}")
            time.sleep(delay_s)

            try:#Intentamos leer corriente
                raw_stepper=stepper.query(":READ?")
                vms, ims = pars_ans(raw_stepper, v_step_prog=SV)
            except Exception: #Intentamos leer tension
                # Fallback simple
                try:
                    raw_stepper_i = stepper.query(":MEAS:CURR?")
                    vms, ims = pars_ans(raw_stepper_i,v_step_prog=SV)
                except Exception as e:
                    print(f"Error en punto {k}:{e}")
                    vms, ims = SV, np.nan
            for j, SW in enumerate(v_sweeper_set,1):
                sweeper.write(f":SOUR:VOLT {SW}")
                time.sleep(delay_s)

                try:#Intentamos leer corriente
                    raw_sweeper=sweeper.query(":READ?")
                    vms_sweep, ims_sweep = pars_ans(raw_sweeper, v_step_prog=SW)
                except Exception: #Intentamos leer tension
                    # Fallback simple
                    try:
                        raw_sweeper_i = sweeper.query(":MEAS:CURR?")
                        vms_sweep, ims_sweep = pars_ans(raw_sweeper_i,v_step_prog=SW)
                    except Exception as e:
                        print(f"Error en punto {j}:{e}")
                        vms_sweep, ims_sweep = SW, np.nan

                vds_meas.append(vms)
                ids_meas.append(ims)

            vg_meas.append(vms)
            
                    
                    
            

            
