import { CognitoUserPool } from "amazon-cognito-identity-js"
const poolData ={
    UserPoolId: 'us-east-1_4ARy8Gy2A',
    ClientId: '6fnn2rt4d1ounb1j9igo65j7bt'
}

export default new CognitoUserPool(poolData)
