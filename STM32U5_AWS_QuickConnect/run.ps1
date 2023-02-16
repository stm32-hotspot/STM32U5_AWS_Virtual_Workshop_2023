
# AWS keys Start

# AWS Keys End


$Env:AWS_REGION="us-east-1"

Clear-Host

python .\STM32U5_AWS_QuickConnect.py --interactive --aws-access-key-id=$env:AWS_ACCESS_KEY_ID --aws-secret-access-key=$env:AWS_SECRET_ACCESS_KEY  --aws-session-token=$env:AWS_SESSION_TOKEN --aws-region=$env:AWS_REGION