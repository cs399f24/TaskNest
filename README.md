# TaskNest


A robust web-based task management application that helps users organize and track their daily tasks with real-time notifications and deadline reminders.
<p align="center">
  <img src="https://github.com/user-attachments/assets/ba11aa6d-223c-4e1e-81e3-1eabb871902b" alt="GIF">
</p>

## Documentation

- Located ad `@/docs/`

## Deployment
- `@` in a file path is referring to the root of the project
- `<Your-Bucket-Name-Here>` when seeing this replace everything including the `<` and `>`.

###### 1. Create s3 bucket with: `@/scripts/create_s3.sh` or according to the documentation.

###### 2. Run up script at `@/up.sh`.
- Make sure AWS ClI is installed and configured

###### 3. Create a Amplify app on the AWS management console
- Steps:
    - Click create new app
    - Click deploy without git
    - type in `s3://<Your-Bucket-Name-Here>/`

## Destruction
###### Run the destroy script `@/scripts/destroy_everything.sh`

## 🌟 Features

- User authentication and authorization
- Real-time task tracking and management
- Deadline notifications using Unix timestamps
- Responsive web interface
- Secure data storage and retrieval

## 🏗️ Architecture

TaskNest is built using a modern cloud-native architecture:

- **Frontend**: React.js application hosted on AWS S3
- **Backend**: Flask REST API running on AWS EC2 (Will be changed to API Gateway Soon)
- **Database**: AWS DynamoDB for scalable data storage
- **Authentication**: AWS Cognito for secure user management
- **Storage**: AWS S3 for static file hosting
- **Notifications**: Real-time alerts based on Unix timestamps

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Python 3.8+
- AWS CLI configured with appropriate credentials
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/cs399f24/TaskNest.git
cd TaskNest
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 📋 Available Scripts

### Frontend Scripts

- `npm start` - Runs the app in development mode at [http://localhost:3000](http://localhost:3000)
- `npm test` - Launches the test runner in interactive watch mode
- `npm run build` - Builds the app for production in the `build` folder

### Backend Scripts

- `flask run` or `python app.py`- Starts the Flask development server


## 🗄️ Database Structure

TaskNest uses DynamoDB with the following schema:

```javascript
{
  "user-id": {
    "S": "DEV_USER"
  },
  "tasks": {
    "L": [
      {
        "M": {
          "description": {
            "S": "test-description"
          },
          "time": {
            "S": "test-time"
          }
        }
      }
    ]
  }
}

```



## 📚 Documentation

Detailed documentation is available for all AWS services used in the project:

- [S3 Configuration](docs/s3.md)
- [EC2 Setup](docs/ec2.md)
- [Cognito Integration](docs/cognito.md)
- [DynamoDB Schema](docs/dynamodb.md)
- [Lambda](docs/lambda.md)
- [AWS Launch Script Guide](docs/launch_aws.md)

## 🚀 Deployment

The application can be deployed using the provided AWS launch script. Refer to the [AWS Launch Script Guide](docs/launch_aws.md) for detailed deployment instructions.

## 🔒 Security

TaskNest implements several security measures:

- AWS Cognito for secure user authentication
- HTTPS encryption for all API communications
- Secure storage of sensitive data in DynamoDB





## 🙏 Acknowledgments

- React.js community
- AWS Documentation
- Flask Documentation
