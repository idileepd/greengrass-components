import { APIGatewayProxyHandler } from "aws-lambda";
import { cognito } from "./provider";

export const handler: APIGatewayProxyHandler = async (event, _context) => {
  try {
    const { USER_POOL_REF, USER_POOL_CLIENT_REF } = process.env;
    const { email, password } = JSON.parse(event.body);
    if (typeof password !== "string" || typeof email !== "string") {
      throw new Error("Invalid Credentials");
    }

    const response = await cognito
      .adminInitiateAuth({
        AuthFlow: "ADMIN_NO_SRP_AUTH",
        UserPoolId: USER_POOL_REF,
        ClientId: USER_POOL_CLIENT_REF,
        AuthParameters: {
          USERNAME: email,
          PASSWORD: password,
        },
      })
      .promise();
    return {
      statusCode: 200,
      body: JSON.stringify({
        ...response.AuthenticationResult,
      }),
    };
  } catch (error) {
    return {
      statusCode: 401,
      body: JSON.stringify({
        error: error,
      }),
    };
  }
};
