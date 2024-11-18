import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { DynamoDB } from "aws-sdk";

const dynamoDb = new DynamoDB.DocumentClient();
const ggDeviceHistory = process.env.GG_DEVICE_HISTORY || "";

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

    const params: DynamoDB.DocumentClient.QueryInput = {
      TableName: ggDeviceHistory,
      IndexName: "ThingIndex", // Use the GSI
      KeyConditionExpression: "sk = :sk",
      ExpressionAttributeValues: {
        ":sk": thingName,
      },
      ScanIndexForward: false, // Sort descending by createdAt
      Limit: 1, // Fetch only the latest record
    };

    const result = await dynamoDb.query(params).promise();
    const item = result.Items ? result.Items[0] : null;

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
