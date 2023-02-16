
#******************************************************************************
# * @file           : BOTO3_cleanupThing.py
# * @brief          : Cleans up thing created by quickConnect.py
# ******************************************************************************
# * @attention
# *
# * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
# * All rights reserved.</center></h2>
# *
# * This software component is licensed by ST under Ultimate Liberty license
# * SLA0044, the "License"; You may not use this file except in compliance with
# * the License. You may obtain a copy of the License at:
# *                             www.st.com/SLA0044
# *
# ******************************************************************************
import boto3
import boto3.session
import sys
import getopt

HELP = ['cleanupThing.py options:', 
        '\n\t-h or --help for help',
        '\n\t--profile=[aws cli profile]', 
        '\n\t--device-id=[device name]',
        '\n\t--version for the file version']

VERSION = "1.3.1"


################################
def getParam(curParam, label):
    param = input(label + " [" + curParam + "]: ").strip()

    if param:
        return param
    else:
        return curParam

################################
def main(argv):
    thing_name = ''
    interactiveMode = False
    PROFILE_NAME = 'default'

    # Collect Parameters from command line
    try:
        opts, args = getopt.getopt(argv,"hi", ["help", "interactive", "version", "profile=", "device-id="])
    except getopt.GetoptError:
        print('Parameter Error')
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(*HELP)
            sys.exit(1)

        elif opt in ("-i"):
            print("Interactive mode")
            PROFILE_NAME = getParam(PROFILE_NAME, "profile name")
            thing_name  = getParam(thing_name, "thing_name")

        elif opt in ("--device-id"):
            thing_name = arg

        elif opt in ("--profile"):
            PROFILE_NAME = arg

        elif opt in ("--version"):
            print("cleanupThing.py version: " + VERSION)
            sys.exit(1)

    if(PROFILE_NAME == ''):
        print("[ERROR] Please specify a profile")
        sys.exit(1)

    if(thing_name == ''):
        print("[ERROR] Please specify a thing name")
        sys.exit(1)

    print("device-id: " + thing_name)
    print("PROFILE_NAME: " + PROFILE_NAME)

    AWS_ACCESS_KEY_ID="ASIAZAPXGKNB3VTJZVAI"
    AWS_SECRET_ACCESS_KEY="DQL57zuIcmgXoUHHHSYros8TP0J+ZHzoCSkXTJSE"
    AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEAkaCXVzLWVhc3QtMSJIMEYCIQCWtzZjM6va9ua3ljlCM3NIjUc39LDfS7xb6OnEJIHf/gIhAKPhT/JIwUQaLZTPWeXLEXWBoYstX+RitE862kfOll88KqICCJL//////////wEQABoMNjE5NTMwNTcyNjExIgzoX8n3yFryNe8XhcYq9gEQcvY9Iy0r0eiMH7kMHQdP295xDdlhH4hnYEwdSysx3zQkHL0MemgqVvTTYoBpYx8Ucr3Qspj3cuxZFZM6w5fX3iZLdCM2GEGbozxUO/FlYwZ+C7DI4NSbrcEJq6tGRdJdvccPrpoBUSna7C2uGzBniGBdy9XVU/FzrtIdTsjYVeR6JrxR8JZ9MjPUNJ8XzKgZDbn977TXEBeaR6Yev0d4koiz+wWmh9BSebTZrlbXksH2n/N7W0T0f9Gys5BgH5xup7L2CG0viHKcgjoriTpZaAGgb98pyjrkzNPGYdrx2sTEACrGnUEyRkno1JoLJLr7TLROoeQwyciUnwY6nAHFpXaCLrEt7qQWwwMsFUMAGrtvHum5VDeBO3Q3+xBLSvqFrHUHLgQ191bLGAb4G8tqdicIPXyHjW8nrVW3ZtdEtieXMC7Ndt8GTRQG9iEFitQAQcAmeGdkfUCU4dzBIAiFzbRZ04o4TvNkamvhJwcresiVtBf/EcWSFdUtEB180eYjepE5Q8YauyusG0T+czS9rLr0idChWCR+Zs0="
    AWS_REGION="us-east-1"

    # Initialize Boto3 resources
    this_session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN, region_name=AWS_REGION)
    #this_session = boto3.session.Session(profile_name=PROFILE_NAME)
    iot = this_session.client('iot')
    
    # Get resources
    thing_found = False
    #while not thing_found:
    try:
            #thing_name = input("Thing name? \n")
            print("Getting:\n")
            cert_arn_list = iot.list_thing_principals(thingName = thing_name)['principals']
            thing_found = True
    except iot.exceptions.ResourceNotFoundException:
            print("Thing " + thing_name + " not found.\n\n")
    
    
    # Building a Dictionary {certArn: [list, of, policies]}
    certDict = {}
    for cert_arn in cert_arn_list:
        print("\tCertificate Arn - " + cert_arn + "\n")

        policy_list = list(map(lambda p: p['policyName'], iot.list_attached_policies(target = cert_arn)['policies']))
        for policy in policy_list:
            print("\t\tPolicy Name - " + policy + "\n")

        certDict[cert_arn] = policy_list

   
    # Detaching certificates 
    for cert_arn in cert_arn_list:
        print("Detaching certificate from thing " + cert_arn + "...\n")
        iot.detach_thing_principal(
            thingName = thing_name, 
            principal = cert_arn
        )

    
    # Detaching every policy from all the attached certs
    for cert_arn in certDict:
        for policy_name in certDict[cert_arn]:
            print("Detaching " + policy_name + " from " + cert_arn + "...\n")
            iot.detach_policy(
                policyName = policy_name, 
                target = cert_arn
            )


    # Deleting the thing
    print("Deleting thing...\n")
    iot.delete_thing(
        thingName = thing_name
    )

    # Deactivating Revoking and Deleting every Cert
    for cert_arn in certDict:
        cert_id = cert_arn.partition('/')[2]
        print("Deactivating certificate " + cert_id + "...\n")
        iot.update_certificate(
            certificateId = cert_id, 
            newStatus = 'INACTIVE'
        )

        print("Revoking certificate...\n")
        iot.update_certificate(
            certificateId = cert_id, 
            newStatus = 'REVOKED'
        )

        print("Deleting certificate...\n")
        iot.delete_certificate(
            certificateId = cert_id
        )
    
    print("Finished.\n")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        print(e)
        sys.exit(1)

#************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/            