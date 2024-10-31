#!/bin/bash
# got rid of outputs using `> /dev/null` because these commands output huge JSON objects
echo Creating security group...
GROUP_ID=$(aws ec2 create-security-group --group-name "task-nest-security-group" \
--description "task-nest-security-group: allows 22, 80" --query 'GroupId' --output text) > /dev/null
echo Created security group with ID: $GROUP_ID

echo Authorizing security group ingress...
aws ec2 authorize-security-group-ingress --group-id "$GROUP_ID" \
--ip-permissions '[
  {"IpProtocol":"tcp","FromPort":22,"ToPort":22,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]},
  {"IpProtocol":"tcp","FromPort":80,"ToPort":80,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]}
]' > /dev/null
echo Authorized.
echo Creating an EC2 instance...
INSTANCE_ID=$(aws ec2 run-instances --image-id "ami-06b21ccaeff8cd686" \
--instance-type "t2.micro" --key-name "vockey" \
--network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["'"$GROUP_ID"'"]}' \
--credit-specification '{"CpuCredits":"standard"}' \
--tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"task-nest-ec2"}]}' \
--metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
--private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
--user-data file://ec2_user_data.sh \
--count "1" --query 'Instances[0].InstanceId' --output text)

echo Waiting for the instance to be in running state...
while true; do
    INSTANCE_STATE=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --query 'Reservations[0].Instances[0].State.Name' --output text)
    
    if [ "$INSTANCE_STATE" == "running" ]; then
        PUBLIC_IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
        if [ "$PUBLIC_IP" != "None" ]; then
            echo "Launched EC2 instance, Public IPv4 address: $PUBLIC_IP"
            break
        else
            echo "Waiting for the public IP address..."
        fi
    else
        echo "."
    fi

    sleep 5
done

echo Building front-end...
# Like this: REACT_APP_EC2_PUBLIC_IP=3.80.214.52
echo "REACT_APP_EC2_PUBLIC_IP=$PUBLIC_IP" >> .env
npm run build > /dev/null
# Exporting environment variables after building so they wont be included in the production build
export SECURITY_GROUP_ID=$GROUP_ID
export EC2_INSTANCE_ID=$INSTANCE_ID
echo Built.

echo Copying build to S3 bucket...
aws s3 cp ./build s3://task-nest-test-bucket-1/ --recursive > /dev/null
echo DONE
