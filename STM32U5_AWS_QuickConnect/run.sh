#!/bin/bash

# AWS keys Start

# AWS Keys End


export AWS_REGION="us-east-1"
export QC_PATH=$(pwd)

python $QC_PATH/STM32U5_AWS_QuickConnect.py --interactive --aws-access-key-id=$AWS_ACCESS_KEY_ID --aws-secret-access-key=$AWS_SECRET_ACCESS_KEY  --aws-session-token=$AWS_SESSION_TOKEN --aws-region=$AWS_REGION