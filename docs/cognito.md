
# AWS Cognito 

1. **Access AWS Console**
   - Navigate to AWS Console
   - Go to Cognito service
   - Click "Manage User Pools"

2. **Create User Pool**
   - Click "Create User Pool" button
   - Name your pool 

3. **Configure Sign-in Options**
   - **Important**: These settings cannot be changed after creation
   - Choose sign-in options:
     - Email address (selected in tutorial)
     - Username
     - Phone number

4. **Attributes**
   - Choose required standard attributes

5. **Password Policy**
   - Set password requirements:
     - Minimum length
     - Require numbers
     - Require special characters
     - Require uppercase letters
     - Require lowercase letters

6. **User Registration**
   - Enable "Allow users to sign themselves up"
   - Skip advanced settings


7. **Message Customization**
   - Choose between verification code or link
   - Customize email subjects and messages

8. **Create App Client**
   - Click "Add an app client"
   - Name your client (e.g., "website")

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




