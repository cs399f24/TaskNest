import { CognitoUserPool } from "amazon-cognito-identity-js"

const poolId = process.env.REACT_APP_USER_POOL_ID
const clientId = process.env.REACT_APP_CLIENT_ID

if (!poolId || !clientId) {
    poolId = 'us-east-1_mWfjt6YIe'
    clientId = '1pkv2b936egtmempn1rou7oalv'
}

const poolData = {
    UserPoolId: poolId,
    ClientId: clientId
}

export default new CognitoUserPool(poolData)
