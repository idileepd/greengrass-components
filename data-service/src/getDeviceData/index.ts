import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { DynamoDB } from "aws-sdk";

const dynamoDb = new DynamoDB.DocumentClient();
const ggDeviceData = process.env.GG_DEVICE_DATA || "";

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  try {
    const thingName =
      event.queryStringParameters?.thingName || process.env.THING_NAME;

    if (!thingName) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          message: "Missing thingName in query parameters.",
        }),
      };
    }

    const params: DynamoDB.DocumentClient.GetItemInput = {
      TableName: ggDeviceData,
      Key: {
        pk: thingName,
      },
    };

    const { Item: item } = await dynamoDb.get(params).promise();

    return {
      statusCode: 200,
      body: JSON.stringify(item || { message: "No records found." }),
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Internal server error." }),
    };
  }
};
