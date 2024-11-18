import { APIGatewayProxyHandler } from "aws-lambda";

export const handler: APIGatewayProxyHandler = async (event, _context) => {
  const {
    USER_POOL_NAME,
    USER_POOL_CLIENT_NAME,
    USER_POOL_REF,
    USER_POOL_CLIENT_REF,
  } = process.env;
  return {
    statusCode: 200,
    body: JSON.stringify({
      message: "Hello, World!",
      USER_POOL_NAME,
      USER_POOL_CLIENT_NAME,
      USER_POOL_REF,
      USER_POOL_CLIENT_REF,
      headers: event.headers,
    }),
  };
};
