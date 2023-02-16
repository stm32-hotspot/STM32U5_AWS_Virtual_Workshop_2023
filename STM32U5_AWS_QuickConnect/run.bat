
@echo off

:: AWS Keys Start

:: AWS Keys End

set AWS_REGION=us-east-1
cls

python .\STM32U5_AWS_QuickConnect.py --interactive --aws-access-key-id=%AWS_ACCESS_KEY_ID% --aws-secret-access-key=%AWS_SECRET_ACCESS_KEY%  --aws-session-token=%AWS_SESSION_TOKEN% --aws-region=us-east-1