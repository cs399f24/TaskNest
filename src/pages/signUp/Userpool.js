import { CognitoUserPool } from "amazon-cognito-identity-js"
const poolData = {
    UserPoolId: 'us-east-1_mWfjt6YIe',
    ClientId: '1pkv2b936egtmempn1rou7oalv'
}

export default new CognitoUserPool(poolData)
