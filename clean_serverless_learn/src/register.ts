import { APIGatewayProxyHandler } from "aws-lambda";

import { cognito } from "./provider";

export const handler: APIGatewayProxyHandler = async (event, _context) => {
  try {
    const { USER_POOL_REF } = process.env;
    const { email, password } = JSON.parse(event.body);
    if (typeof password !== "string" || typeof email !== "string") {
      throw new Error("Invalid Credentials");
    }

    const result = await cognito
      .adminCreateUser({
        UserPoolId: USER_POOL_REF,
        Username: email,
        UserAttributes: [
          {
            Name: "email",
            Value: email,
          },
          {
            Name: "email_verified",
            Value: "true",
          },
        ],
        //   we don't want to send email
        MessageAction: "SUPPRESS",
      })
      .promise();

    if (!result.User) {
      throw new Error("Unable to create user");
    }

    await cognito
      .adminSetUserPassword({
        Password: password,
        UserPoolId: USER_POOL_REF,
        Username: email,
        Permanent: true,
      })
      .promise();

    return {
      statusCode: 200,
      body: JSON.stringify({
        result,
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
