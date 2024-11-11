
# AWS Cognito 

1. **Access AWS Console**
   - Navigate to AWS Console
   - Click on User pools

2. **Create User Pool**
   - Click "Create User Pool" button
     
3. **Configure Sign-in Options**
   - Choose email only

4. **Password Policy**
   - Cognito defaults
   - No MFA
   - Uncheck user account recovery

5. **Configure sign-up experience**
   - Leave everything there default


6. **Configure message delivery**
   - Send email with Cognito

7. **Integrate Your App**
    - Name your pool "task-user-pool"
    - Name your client "task-app-client"
   
8. **Review and create**
    - You should be good now and can press create user pool
   
   


## For The React Integration

1. **Install Required Package**
```bash
npm install amazon-cognito-identity-js
```

2. **Create UserPool.js**
```javascript
import { CognitoUserPool } from "amazon-cognito-identity-js";

const poolData = {
    UserPoolId: "<your-user-pool-id>", // From Cognito General Settings
    ClientId: "<your-client-id>"       // From App Client Settings
};

export default new CognitoUserPool(poolData);
```




