
# Sign in
In a browser navigate to https://aws.amazon.com/
and click on the `Sign In to the Console` button.

Enter the received account ID, username, and password.
Upon first login, you have to change the password.

# Launch an Virtual Computer
In Management Console, click on the search bar.
Search and select the service: `EC2`
Verify that you are using the previously agreed region.
In the navigation menu find the group `Instances` and select `Instances`.
Click on Launch instances and configure as follows:
Name: `******************`
* Application and OS Images: from quickstart select Amazon Linux
* Instance type: t2.micro
* Key pair: proceed without a key pair
* Network setting: leave it on default
* Configure storage: leave it on default

Once successfully initiated the launch,
In the navigation menu find the group 'Instances' and select 'Instances'.
From the list, find your new virtual instance, click on the instance ID.
On the bottom menu select on Tags, and click on Manage Tags, And a new tag with:
* Key: `Owner`
* Value: `[YOUR NAME]`

## Connect to the Virtual Computer

Once successfully initiated the launch,
In the navigation menu find the group 'Instances' and select 'Instances'.
From the list, find your new virtual instance, click on the instance ID.
On the top click on Connect, select EC2 Instance Connect.
Now you have two (or more) browser tabs to the account.

## Use the Virtual Computer

Install MLflow
```bash
sudo yum update -y
sudo yum install python3 -y
python3 --version
sudo yum -y install python-pip
pip --version
sudo pip install mlflow --ignore-installed
sudo yum install httpd-tools -y
sudo yum install nginx -y
```

Create a user and a password
```bash
sudo htpasswd -c /etc/nginx/.htpasswd [SOME_USERNAME]
```

Configure nginx to reverse proxy to port 5000
```bash
sudo nano -c /etc/nginx/nginx.conf
```
add the following in the block `server {}` around line 43
```bash
        location / {
        proxy_pass http://0.0.0.0:5000/;
        auth_basic "Restricted Content";
        auth_basic_user_file /etc/nginx/.htpasswd;
        }
```
exit with Ctrl+X, save with Y, Enter to confirm name.

Launch MLflow
```bash
sudo service nginx start
mlflow server --host 0.0.0.0 --port 5000
```

Select a different browser tab.
In Management Console, click on the search bar.
Search and select the service: EC2
In the navigation menu find the group 'Instances' and select 'Instances'.
From the list, find the instance, click on the instance ID.

Click on the Security tab and click on the security group.
Once in the Security Group attached to the EC2 click on Edit inbound rules
Add rule:
* Type: HTTP
* Source: Custom: 0.0.0.0/0 (even better to use your ip, https://www.myip.com/, or google "What's my IP")
* Description: `open up for HTTP requests`
Click on Save rules

## Virtual Computer as a remote server

Select a different browser tab.
In Management Console, click on the search bar.
Search and select the service: EC2
In the navigation menu find the group 'Instances' and select 'Instances'.
From the list, find the instance, click on the instance ID.
Search for Public IPv4 address and open a new browser tab:
`http://[PUBLIC_IPv4_ADDRESS]/`

Stop your instance
Note: Your instance’s public IP address will change each time you stop & restart it. Unless… you decide to use an elastic IP address: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html


# Programmatic access

This section uses your local computer.

## Get your credentials
In Management Console, click on the search bar.
Search and select the service: Identity and Access Management (IAM)
From the navigation menu select 'Users'.
Find your username and select it.
Got to tabe 'Security credentials'.
Under Access keys, click on 'Create access key'.
Save the values of `aws_access_key_id` and `aws_secret_access_key`.

Dowload AWS CLI (version 2)
https://aws.amazon.com/cli/
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html


## Store your credentials

Configure your AWS credentials
```bash
aws configure
```
Reference: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
Default region: name enter the previously agreed region 
Default output format: press Enter to leave it blank

Note the content of the folder `~/.aws`

on Unix
```bash
cat ~/.aws/credentials
cat ~/.aws/config
```

on Windows
```batch
type ~/.aws/credentials
type ~/.aws/config
```

Configure a named profile with the same parameters
```bash
aws configure --profile ********
```

Expected output:

~/.aws/credentials
```bash
[profile default]
region=eu-west-1

[profile ********]
region=eu-west-1
```

~/.aws/config
```bash
[default]
aws_access_key_id=************
aws_secret_access_key=************

[knos-ai]
aws_access_key_id=************
aws_secret_access_key=************
```

## Use the programmatic access

Try
```bash
aws s3 ls
aws ec2 describe-instances --region eu-west-1 --profile ************
```

Troubleshooting:
1. Error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
Resolution configure enviroment variable to point to .pem
Workaround for this training append `--no-verify-ssl`

# Terminate your resource

Terminate all resources that you have created during this session.