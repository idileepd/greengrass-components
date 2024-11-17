import sys
import os
import src.greeter as greeter
import time

import boto3



def getAwsInfo():
    device_info = {
        'thing_name': os.environ.get('AWS_IOT_THING_NAME'),
        'aws_region': os.environ.get('AWS_REGION'),
    }
    
    # # Print available information
    # for key, value in device_info.items():
    #     if value:
    #         print(f"{key}: {value}")
    #     else:
    #         print(f"{key} not available")
            
    return device_info

print("Hello 9999")

def main():
    args = sys.argv[1:]
    print("kkkkkkkkk Command-line arguments:", args)    
    while True:
        print("\n\n*********")
        greeting = greeter.get_greeting(" ".join(args))
        print("Greeting:", greeting)
        print(getAwsInfo())
        region = boto3.session.Session().region_name
        print(f"%%%%%%%%%%%%Region: {region}")

        sts_client = boto3.client("sts")
        account_id = sts_client.get_caller_identity()["Account"]
        print(f"%%%%%%%%%%%%Account ID: {account_id}")

        time.sleep(5)
if __name__ == "__main__":
    main()

# import os
# import json
# import awsiot.greengrasscoreipc
# import awsiot.greengrasscoreipc.client as client
# from awsiot.greengrasscoreipc.model import (
#     GetThingNameRequest,
#     SubscribeToIoTCoreRequest,
#     PublishToIoTCoreRequest
# )

# TIMEOUT = 10

# def get_device_info():
#     try:
#         # Initialize IPC client
#         ipc_client = awsiot.greengrasscoreipc.connect()
        
#         # Get thing name using IPC
#         thing_name_request = GetThingNameRequest()
#         thing_name_response = ipc_client.get_thing_name(thing_name_request)
#         thing_name = thing_name_response.thing_name
        
#         # Get other environment variables
#         device_info = {
#             'thing_name': thing_name,
#             'aws_region': os.environ.get('AWS_REGION'),
#             'account_id': os.environ.get('AWS_ACCOUNT_ID', ''),
#             'gg_component_name': os.environ.get('AWS_GREENGRASS_COMPONENT_NAME', ''),
#             'gg_root': os.environ.get('AWS_GREENGRASS_ROOT', '')
#         }
        
#         print("Device Info:", json.dumps(device_info, indent=2))
#         return device_info
        
#     except Exception as e:
#         print(f"Error getting device info: {str(e)}")
#         return None

# def main():
#     # Get device information
#     device_info = get_device_info()
    
#     if device_info:
#         print(f"Successfully retrieved device info for thing: {device_info['thing_name']}")
#     else:
#         print("Failed to get device information")

# if __name__ == '__main__':
#     main()