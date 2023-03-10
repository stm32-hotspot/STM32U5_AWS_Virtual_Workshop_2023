#******************************************************************************
# * @file           : getDeviceName.py
# * @brief          : Get the device name
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

import serial, serial.tools.list_ports
import sys
from uuid import getnode as get_mac


def get_name():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "VID:PID=0483:374" in p.hwid:
            mac = get_mac()
            device_id = 'stm32u5-' + hex(mac)[-5:-1] + p.serial_number[-10:] + p.device[-2:]
            return device_id
    
    raise Exception("Port Error")

def main():
    device_id = get_name()
    print(device_id)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)

#************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/                