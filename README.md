# AWS CloudWatch Alarms Testing

This project contains a CloudFormation template that creates a set of CloudWatch alarms for an AWS Lambda function, and a Bash script that triggers the Lambda function and periodically checks the state of the alarms.

The CloudFormation template (`cloudformation_template.yaml`) creates:

- An AWS Lambda function that returns a simple "Hello, World!" message.
- Eight CloudWatch alarms with different configurations to test how CloudWatch alarms behave under different settings.

The Bash script (`check_alarms.sh`):

- Triggers the Lambda function every minute.
- Checks the state of each CloudWatch alarm every 10 seconds.
- Outputs the time elapsed since the script started, the current state of each alarm, and the time when the alarm state last changed.

## Usage

### Deploy the CloudFormation stack

1. Navigate to the AWS Management Console, and open the CloudFormation service.
2. Click "Create stack", and choose "With new resources".
3. Choose "Upload a template file", and upload the `cloudformation_template.yaml` file from this repository.
4. Click "Next", and fill in the stack name and parameters as required.
5. Click "Next", review your settings, and then click "Create stack".

### Run the Bash script

1. Open a terminal.
2. Navigate to the directory where the `check_alarms.sh` script is located.
3. Run the script by entering `./check_alarms.sh` followed by the name of your Lambda function, for example `./check_alarms.sh my-lambda-function`. If you don't provide the name of the Lambda function as an argument, the script will prompt you for it.
4. The script will run indefinitely, triggering the Lambda function every minute and checking the state of the alarms every 10 seconds. To stop the script, press `Ctrl+C`.

## Prerequisites

- AWS account with permissions to create and manage CloudFormation stacks, Lambda functions, and CloudWatch alarms.
- AWS CLI installed and configured with your AWS account credentials.
- Bash shell to run the script.
