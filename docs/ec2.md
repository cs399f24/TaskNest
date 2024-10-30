# EC2
- Name: `task-nest-ec2`
- Note: When launching the system when using AWS Learner Lab even if you don't terminate a EC2 instance hosting the back-end when the learner lab is relaunched the IPv4 address will change.
- Instance Type: `t2.micro`
- Key Name: `vockey` (The `.pem` file can be downloaded from aws details in the learner lab)
- Uses the default `VPC`, subject to change.
- Create a new Security group is chosen
- #### Security Group
    - Name: `task-nest-security-group`
    - Ports enabled: `22`(SSH), and `80`(HTTP)
- Following are commands to create this instance and are to be executed in order found on this document:
```bash
aws ec2 create-security-group --group-name "task-nest-security-group" \
--description "task-nest-security-group: allows 22, 80" \
--vpc-id "vpc-0df1909ea8ee1046a"
```
```bash
aws ec2 authorize-security-group-ingress --group-id "sg-preview-1" \
--ip-permissions '{"IpProtocol":"tcp","FromPort":22,"ToPort":22,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]}' \
'{"IpProtocol":"tcp","FromPort":80,"ToPort":80,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]}'
```
```bash
aws ec2 run-instances --image-id "ami-06b21ccaeff8cd686" \
--instance-type "t2.micro" --key-name "vockey" \
--network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["sg-preview-1"]}' \
--credit-specification '{"CpuCredits":"standard"}' \
--tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"task-nest-ec2"}]}' \
--metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
--private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
--count "1"
```