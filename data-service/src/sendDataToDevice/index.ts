import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { IotData } from "aws-sdk";

// Interfaces
interface PublishRequest {
  thingName?: string;
  metadata: Record<string, any>;
}

interface PublishResponse {
  message: string;
  topic: string;
}

interface ErrorResponse {
  error: string;
  details: string;
}

// Initialize AWS IoT Data
const iotdata = new IotData({
  endpoint: process.env.IOT_ENDPOINT,
  region: process.env.REGION,
});

// Common response headers
const headers = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Credentials": true,
};

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  try {
    if (!event.body) {
      throw new Error("Request body is missing");
    }

    // Parse and validate the request body
    const body: PublishRequest = JSON.parse(event.body);

    if (!body.thingName) {
      throw new Error("thingName is required in the request body");
    }

    if (!body.metadata) {
      throw new Error("Metadata is required in the request body");
    }

    // Construct the topic dynamically
    const topic = `/${body.thingName}/device-listen`;

    // Parameters for publishing to IoT Core
    const params: IotData.PublishRequest = {
      topic,
      payload: JSON.stringify(body.metadata),
      qos: 0,
    };

    // Publish the message
    await iotdata.publish(params).promise();

    const response: PublishResponse = {
      message: "Message published successfully",
      topic,
    };

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(response),
    };
  } catch (error) {
    console.error("Error:", error);

    const errorResponse: ErrorResponse = {
      error: "Failed to publish message",
      details:
        error instanceof Error ? error.message : "Unknown error occurred",
    };

    return {
      statusCode: 500,
      headers,
      body: JSON.stringify(errorResponse),
    };
  }
};
