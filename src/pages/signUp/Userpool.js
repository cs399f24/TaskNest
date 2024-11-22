import { CognitoUserPool } from "amazon-cognito-identity-js"
const poolData ={
    UserPoolId: 'us-east-1_whAnFO9WL',
    ClientId: '7s4n8gron4g0ep0mu8kkkm16dn'
}

export default new CognitoUserPool(poolData)
