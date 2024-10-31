# Launch_aws.sh
To use The launch script you will meed to have `AWS CLI` installed as well as `NodeJS`
#### General steps took in the `Launch.sh` script:
```bash
GROUP_ID=$(aws ec2 create-security-group --group-name "task-nest-security-group" \
--description "task-nest-security-group: allows 22, 80" --query 'GroupId' --output text) > /dev/null
```
- Creates a security group.
- Declaring a variable name `GROUP_ID` and storing the output of the command in it.
- Create a AWS Security Group using `aws ec2 create-security-group`
###### Flags:
- `--group-name` specifies the name ot create the security group under.
- `--description` specifies the description of the security group being created.
- `--query` a flag querying the output of the command to return a certain piece of the output.
- `--output` a flag for the user to specify what kind of output they want `JSON` is default.
###### Extras:
- `> /dev/null` at the end reroutes the extra output of the command into a nonexistent directory to get rid of it. (Note: when rerouting to `/dev/null` all output is routed **EXCEPT** the errors.)
--------------------------------------------------
```bash
aws ec2 authorize-security-group-ingress --group-id "$GROUP_ID" \
--ip-permissions '[
  {"IpProtocol":"tcp","FromPort":22,"ToPort":22,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]},
  {"IpProtocol":"tcp","FromPort":80,"ToPort":80,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]}
]' > /dev/null
```
- Authorizes inbound connections through the security group into port 22, and 80
- `--group-id` Specify the security group id to modify
- `--ip-permissions` in json format like the following to specify the ports:
```json
[
  {"IpProtocol":"tcp","FromPort":22,"ToPort":22,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]},
  {"IpProtocol":"tcp","FromPort":80,"ToPort":80,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]}
]
```
- `> /dev/null` at the end reroutes the extra output of the command into a nonexistent directory to get rid of it. (Note: when rerouting to `/dev/null` all output is routed **EXCEPT** the errors.)
--------------------------------------------------
```bash
INSTANCE_ID=$(aws ec2 run-instances --image-id "ami-06b21ccaeff8cd686" \
--instance-type "t2.micro" --key-name "vockey" \
--network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["'"$GROUP_ID"'"]}' \
--credit-specification '{"CpuCredits":"standard"}' \
--tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"task-nest-ec2"}]}' \
--metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
--private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
--user-data file://ec2_user_data.sh \
--count "1" --query 'Instances[0].InstanceId' --output text)
```
- Creates an EC2 instance.
- Declaring a variable name INSTANCE_ID and storing the output of the command in it.
- Create an AWS EC2 instance using aws ec2 run-instances.
###### Flags:
- `--image-id` Specifies the ID of the AMI to use for the instance.
- `--instance-type` Specifies the instance type.
- `--key-name` Specifies the name of the ssh key pair.
- `--network-interfaces`:
    - `AssociatePublicIpAddress` Indicates whether to associate a public IP address.
    - `DeviceIndex` Specifies the index of the network interface.
    -  `Groups` Specifies the security groups to associate with the instance.
- `--credit-specification`:
    - `CpuCredits`: Defines the type of CPU credits (e.g., standard).
- `--tag-specifications`:
    - `Tags` An array of key-value pairs to tag the instance.
- `--metadata-options`:
    - `HttpEndpoint` Enables the metadata service endpoint.
    - `HttpPutResponseHopLimit` Limits the number of hops for HTTP PUT requests.
    - `HttpTokens` Requires the use of session tokens to access the metadata service.
- `--private-dns-name-options`:
    - `HostnameType` Specifies how the hostname is generated.
    - `EnableResourceNameDnsARecord` Enables an A record in Route 53.
    - `EnableResourceNameDnsAAAARecord` Enables an AAAA record in Route 53.
- `--user-data` Specifies the file to be used for instance initialization (bootstrapping).
- `--count` Indicates how many instances to launch (in this case, 1).
- `--query` A flag querying the output to return a specific piece of data.
- `--output` A flag to specify the format of the output, the default is `JSON`.
--------------------------------------------------