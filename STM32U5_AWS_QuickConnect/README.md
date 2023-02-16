# STM32U5_AWS_QuickConnect

## Hardware requirements
[B-U585I-IOT02A](https://estore.st.com/en/b-u585i-iot02a-cpn.html)

## Software requirements
* Clone the repo 
```
    git clone https://github.com/SlimJallouli/STM32U5_AWS_QuickConnect.git
```
* Install [AWS CLI](https://aws.amazon.com/cli/)
* Install [python](https://www.python.org/downloads/)
* run **pip install -r requirements.txt**

* Sign in to [AWS console](https://console.aws.amazon.com/console/home)
* Create 2 IAM users
    * First usesr with the **AWSIoTFullAccess** policy. This IAM user will be used to register the device with AWS IoT core (used with the **provision** AWS CLI profile)
    
    * Second user with the following policy (used with the **dash_board** AWS CLI profile)

```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "iot:Receive",
                    "iot:ListNamedShadowsForThing",
                    "iot:Subscribe",
                    "iot:Connect",
                    "iot:GetThingShadow",
                    "iot:DeleteThingShadow",
                    "iot:UpdateThingShadow",
                    "iot:Publish"
                ],
                "Resource": [
                    "arn:aws:iot:<your-region>:<your-account-number>:topic/*",
                    "arn:aws:iot:<your-region>:<your-account-number>:topic/$aws/things/*",
                    "arn:aws:iot:<your-region>:<your-account-number>:client/*",
                    "arn:aws:iot:<your-region>:<your-account-number>:thing/*",
                    "arn:aws:iot:<your-region>:<your-account-number>:topicfilter/*"
                ]
            }
        ]
    }
```



* Use AWS CLI to create 2 profiles (example **provision** and **dash_board**)
* Connect the board to you computer
* Call the STM32U5_AWS_QuickConnect.py as following

```
python .\STM32U5_AWS_QuickConnect.py --ssid=<YOUR_2.4HGz_WIFI_SSID> --password=<YOUR_WIFI_PASSWORD> --dashboard-profile=<AWS_CLI_DASHBOARD_PROFILE> --provision-profile=<AWS_CLI_PROVISION_PROFILE> --dashboard-url=<DASHBOARD_URL>
```


## Example:
```
python .\STM32U5_AWS_QuickConnect.py --ssid=st_iot_demo --password=stm32u585 --dashboard-profile=dash_board --provision-profile=default --dashboard-url=https://main.3mkj47qkab3qo.amplifyapp.com
```
