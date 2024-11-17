import boto3
import uuid
from decimal import Decimal
from botocore.exceptions import ClientError


class DynamoDBUtil:
    def __init__(self, table_name: str, thing_name: str):
        """
        Initializes the DynamoDB utility.

        :param table_name: Name of the DynamoDB table.
        :param thing_name: Thing name to be used as the `sk` for the records.
        """
        self.table_name = table_name
        self.thing_name = thing_name
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def _convert_floats_to_decimals(self, data: dict) -> dict:
        """
        Recursively converts all float values in a dictionary to Decimal.

        :param data: The input dictionary.
        :return: A new dictionary with floats replaced by Decimals.
        """
        if isinstance(data, dict):
            return {k: self._convert_floats_to_decimals(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_floats_to_decimals(v) for v in data]
        elif isinstance(data, float):
            return Decimal(str(data))  # Convert float to Decimal preserving precision
        return data

    def add_record(self, data: dict) -> str:
        """
        Adds a new record to the DynamoDB table.

        :param data: A dictionary of additional fields to add.
        :return: The generated UUID used as the `pk`.
        """
        pk = str(uuid.uuid4())
        item = {
            "pk": pk,
            "sk": self.thing_name,
            **self._convert_floats_to_decimals(data),
        }

        try:
            self.table.put_item(Item=item)
            print(f"Record added successfully: {item}")
            return pk
        except ClientError as e:
            print(f"Error adding record: {e.response['Error']['Message']}")
            raise

    def update_record(self, pk: str, update_data: dict) -> None:
        """
        Updates an existing record in the DynamoDB table.

        :param pk: The primary key (`pk`) of the record to update.
        :param update_data: A dictionary of fields to update with new values.
        """
        update_data = self._convert_floats_to_decimals(update_data)
        update_expression = "SET " + ", ".join(
            [f"#{k}=:{k}" for k in update_data.keys()]
        )
        expression_attribute_names = {f"#{k}": k for k in update_data.keys()}
        expression_attribute_values = {f":{k}": v for k, v in update_data.items()}

        try:
            response = self.table.update_item(
                Key={"pk": pk, "sk": self.thing_name},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW",
            )
            print(f"Record updated successfully: {response['Attributes']}")
        except ClientError as e:
            print(f"Error updating record: {e.response['Error']['Message']}")
            raise
