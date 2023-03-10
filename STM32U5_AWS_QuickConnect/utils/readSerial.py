#******************************************************************************
# * @file           : readSerial.py
# * @brief          : Read from the serial port and print on the console
# ******************************************************************************
# * @attention
# *
# * <h2><center>&copy; Copyright (c) 2022 STMicroelectronics.
# * All rights reserved.</center></h2>
# *
# * This software component is licensed by ST under BSD 3-Clause license,
# * the "License"; You may not use this file except in compliance with the
# * License. You may obtain a copy of the License at:
# *                        opensource.org/licenses/BSD-3-Clause
# ******************************************************************************
import serial
import serial.tools.list_ports
import time

# Finds and returns the port for the connected board.
def get_com():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "VID:PID=0483:374" in p.hwid:
            return p.device
    
    return " PORT ERR "
            
# Read a line from serial port
def read_line(ser):
    line = ser.readline().decode("utf-8", errors='ignore')
    return line

# Wait for STM32 to connect to AWS
def wait_for_stm32_connection(COM):
    ser = serial.Serial(COM, 115200)
    stm32_ok_found = False
    while stm32_ok_found == False:
        line = read_line(ser)
        #print(line, end = '')

        if "[MQTTAgent ] Connected socket:" in line:
            stm32_ok_found = True
            time.sleep(1)

# Indefinitely read serial communication
def serial_reader(COM):
    ser = serial.Serial(COM, 115200)

    #reading serial port indefinitely
    try:
        while True:
            if ser.in_waiting > 0:
                print(ser.readline().decode("utf-8", errors='ignore'), end = '')
                
            else: 
                time.sleep(1)
    except KeyboardInterrupt:
        quit()
        

if __name__ == "__main__":
    #serial_reader(get_com())
    wait_for_stm32_connection(get_com())


#************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/        
