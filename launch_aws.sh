# got rid of outputs using `> /dev/null` because these commands output huge JSON objects
echo Creating an EC2 instance...
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

INSTANCE_ID=$(aws ec2 run-instances --image-id "ami-06b21ccaeff8cd686" \
--instance-type "t2.micro" --key-name "vockey" \
--network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["'"$GROUP_ID"'"]}' \
--credit-specification '{"CpuCredits":"standard"}' \
--tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"task-nest-ec2"}]}' \
--metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
--private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
--count "1" --query 'Instances[0].InstanceId' --output text)

# Using `describe-instances` to get the ip address so it can be loaded into an environment variable
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
echo "Launched EC2 instance, Public IPv4 address: $PUBLIC_IP"

export EC2_PUBLIC_IP=$PUBLIC_IP npm run build
