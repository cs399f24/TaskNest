import { CognitoUserPool } from "amazon-cognito-identity-js"
const poolData ={

    UserPoolId: 'us-east-1_AL2BDiVkI',
    ClientId: '256ur23d0d83olrm25ei3e1913'

   
}

export default new CognitoUserPool(poolData)