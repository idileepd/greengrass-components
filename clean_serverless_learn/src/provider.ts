import { CognitoIdentityServiceProvider } from "aws-sdk";

export const cognito = new CognitoIdentityServiceProvider();

// Endpoints
// https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FDyGrrjP6/.well-known/openid-configuration
//
// OUTPUT :::::::
//  {
//     "authorization_endpoint": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FDyGrrjP6/authorize",
//     "end_session_endpoint": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FDyGrrjP6/logout",
//     "id_token_signing_alg_values_supported": [
//       "RS256"
//     ],
//     "issuer": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FDyGrrjP6",
//     "jwks_uri": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FDyGrrjP6/.well-known/jwks.json",
//     "response_types_supported": [
//       "code",
//       "token"
//     ],
//     "revocation_endpoint": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FDyGrrjP6/revoke",
//     "scopes_supported": [
//       "openid",
//       "email",
//       "phone",
//       "profile"
//     ],
//     "subject_types_supported": [
//       "public"
//     ],
//     "token_endpoint": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FDyGrrjP6/token",
//     "token_endpoint_auth_methods_supported": [
//       "client_secret_basic",
//       "client_secret_post"
//     ],
//     "userinfo_endpoint": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_FDyGrrjP6/userInfo"
//   }
