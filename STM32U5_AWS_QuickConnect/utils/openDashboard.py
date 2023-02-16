#******************************************************************************
# * @file           : openDashBoard.py
# * @brief          : generate the link to the dashboard and open the link in the browser
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

AWS_CLI_DASHBOARD_PROFILE = 'dashboard'
 

HELP = ['openDashboard.py options:', 
        '\n\t-h or --help for help',
        '\n\t--dashboard-profile=[aws cli dashboard profile]', 
        '\n\t--device-id=[device name]']


def main(argv):
    AWS_CLI_DASHBOARD_PROFILE = "dash_board"

    deviceName = ''
    bucketURL = ''

    # Collect Parameters from command line
    try:
        opts, args = getopt.getopt(argv,"h", ["help", "dashboard-profile=", "device-id=", "dashboard-url="])
    except getopt.GetoptError:
        print('Parameter Error')
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(*HELP)
            sys.exit(1)
        
        elif opt in ("--dashboard-profile"):
            AWS_CLI_DASHBOARD_PROFILE = arg
            # Initialize Boto3 resources
            this_session = boto3.session.Session(profile_name=AWS_CLI_DASHBOARD_PROFILE)
            credentials = this_session.get_credentials()
            frozen_credentials = credentials.get_frozen_credentials()
            key = frozen_credentials.access_key
            secretKey = frozen_credentials.secret_key

        elif opt in ("--key-id"):
            key = arg

        elif opt in ("--secret-key"):
            secretKey = arg

        elif opt in ("--device-id"):
            deviceName = arg

        elif opt in ("--dashboard-url"):
            bucketURL = arg


    webbrowser.open(bucketURL)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        print(e)
        sys.exit(1)

#************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/                