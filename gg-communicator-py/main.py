import sys
import os
import src.greeter as greeter
import time
import boto3
from src.dynamodb_util import DynamoDBUtil


def getAwsInfo():
    try:
        # region = boto3.session.Session().region_name
        sts_client = boto3.client("sts")
        account_id = sts_client.get_caller_identity()["Account"]

        device_info = {
            "thing_name": os.environ.get("AWS_IOT_THING_NAME"),
            "aws_region": os.environ.get("AWS_REGION"),
            "aws_account_id": account_id,
        }
        return device_info
    except:
        print("An exception occurred getting aws info")
        return {}


def run_test():
    # try:
    # Initialize the utility
    dynamodb_util = DynamoDBUtil(table_name="gg-devices-data", thing_name="MyThingName")

    # Add a record
    data_to_add = {"temperature": 22.5, "humidity": 60}
    pk = dynamodb_util.add_record(data=data_to_add)
    print(f"Added record with PK: {pk}")

    # Update a record
    update_data = {"temperature": 24.0}
    dynamodb_util.update_record(pk=pk, update_data=update_data)
    print(f"Updated record with PK: {pk}")
    # except:
    #     print("Error Dynamodb")


def main():
    args = sys.argv[1:]
    while True:
        print("::: args - ", args)
        print("::: aws info", getAwsInfo())
        run_test()

        time.sleep(20)


if __name__ == "__main__":
    main()
