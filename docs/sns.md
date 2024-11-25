# AmazonSNS

1. **Get to Amazon sns**
- Go to the services platform on the AWS website and type "SNS"
- Click on AWS sns and type your topic name under "Create Topic"
- Select the "Next Step" button

2. **Configure Amazon sns**
- Under details, select Standard
- Keep everything else on default
- Click "Create Topic" button at the bottom of the page

3. **Code & sns**
- Double check in sns.py, that you are accessing the correct sns topic
- The Topic Name is found in the line of code below

    "response = sns_client.create_topic(Name='TaskNoti')"

- Change the topic name in the code to match yours "Name='<YourTopicName>'"
