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
    const limit = parseInt(event.queryStringParameters?.limit || "10", 10);

    if (!thingName) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          message: "Missing thingName in query parameters.",
        }),
      };
    }

    if (isNaN(limit) || limit <= 0) {
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Limit must be a positive number." }),
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
      Limit: limit, // Limit the number of records
    };

    const result = await dynamoDb.query(params).promise();

    return {
      statusCode: 200,
      body: JSON.stringify(result.Items || []),
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Internal server error." }),
    };
  }
};
