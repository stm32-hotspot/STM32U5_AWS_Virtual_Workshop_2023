#******************************************************************************
# * @file           : getConfig.py
# * @brief          : Get the device configuration to be used in the Keil Studio project
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
import os, sys
import getopt
import webbrowser

import boto3
import boto3.session

HELP = ['openDashboard.py options:', 
        '\n\t-h or --help for help',
        '\n\t--profile=[aws cli dashboard profile]', 
        '\n\t--device-id=[device name]',
        '\n\t--wifi-ssid=[WiFi SSID]', 
        '\n\t--wifi-credential=[WiFi Password]']


def main(argv):
    AWS_CLI_DASHBOARD_PROFILE = "default"
    deviceName = ''
    wifi_ssid = ''
    wifi_password = ''
    keil_studio_url='https://studio.keil.arm.com/auth/login/'
    git_url='https://github.com/ConstantlySorrowful/aws_mqtt_mutualauth_demo.git'

    # Collect Parameters from command line
    try:
        opts, args = getopt.getopt(argv,"h", ["help", "profile=", "device-id=", "wifi-ssid=", "wifi-credential="])
    except getopt.GetoptError:
        print('Parameter Error')
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(*HELP)
            sys.exit(1)
        
        elif opt in ("--profile"):
            AWS_CLI_DASHBOARD_PROFILE = arg
            # Initialize Boto3 resources
            this_session = boto3.session.Session(profile_name=AWS_CLI_DASHBOARD_PROFILE)
            credentials = this_session.get_credentials()
            frozen_credentials = credentials.get_frozen_credentials()
            key = frozen_credentials.access_key
            secretKey = frozen_credentials.secret_key

        elif opt in ("--device-id"):
            deviceName = arg
            
        elif opt in ("--wifi-ssid"):
            wifi_ssid = arg

        elif opt in ("--wifi-credential"):
            wifi_password = arg

    # Initialize Boto3 resources
    this_session = boto3.session.Session(profile_name=AWS_CLI_DASHBOARD_PROFILE)
    credentials = this_session.get_credentials()
    frozen_credentials = credentials.get_frozen_credentials()

    key = frozen_credentials.access_key
    secretKey = frozen_credentials.secret_key
    
    my_session = boto3.session.Session(profile_name=AWS_CLI_DASHBOARD_PROFILE)
    REGION = my_session.region_name 
    #print(REGION)   

    iot_client = boto3.client('iot', region_name=REGION)
    endpoint_response = iot_client.describe_endpoint(endpointType='iot:Data-ATS')
    IOT_ENDPOINT = endpoint_response['endpointAddress']
    #print(IOT_ENDPOINT)  
    

    with open('config.txt', 'w') as f:
        f.write("keil_studio_url:    " + keil_studio_url + '\n\n')

        f.write("git_url:     " + git_url + '\n\n')
        
        f.write("key=" + key + '\n')
        f.write("secretKey=" + secretKey + '\n\n')

        f.write('export MQTT_BROKER_ENDPOINT=' + IOT_ENDPOINT +'\n')
        f.write('export IOT_THING_NAME=' + deviceName + '\n')
        f.write('export WIFI_SSID=' + wifi_ssid + '\n')
        f.write('export WIFI_PASSWORD=' + wifi_password + '\n')
        f.close()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        print(e)
        sys.exit(1)

#************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/                