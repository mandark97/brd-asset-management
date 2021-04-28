![master](https://github.com/alin-grecu/asset-management/actions/workflows/main.yml/badge.svg)

# BRD Asset Management

## Introduction

* This is a simple Python script and Jinja2 template that allows you to leverage AWS Lambda and AWS SES (Simple Email Service) to send various metrics about your BRD Asset Management portfolios.  
  
* The scripts is now configured for BRD Simfonia and BRD Diverso A, but feel free to fork and add or remove portfolios.

## Architecture

1. Amazon EventBridge
    * Used for the cron MON-FRI at 08:00 EEST.

2. Amazon Lambda
    * Code is hosted in Lambda as a function and gets executed when EventBridge trigger is activated.

3. Amazon Simple Email Service
    * Python script connects to SES and sends the email with all the information.

## Configuration

### Requirements

1. **AWS Account** - For AWS Lambda and AWS SES.
2. **IAM User** - You will use the Access Key ID and Secret from this user with GitHub Actions to deploy the code on Lambda. 
3. **AWS Lambda Function** - You can check this guide [here.](https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html)
4. **AWS EventBridge** - I configured this to be a simple cron from MON-FRI at 08:00 EEST. You can check how to configure and link AWS EventBridge to AWS Lambda [here](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html).
5. **AWS Lambda Function Layer** - Create a layer to install function dependencies, here's a [guide](https://medium.com/the-cloud-architect/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d).
6. **AWS SES** - I use a domain for this that needs to be verified and the email address you want to send to also validated. You can check a guide on AWS SES [here](https://docs.bitnami.com/aws/how-to/use-ses/).

**[NOTE]**: To the IAM user you need to attach **AWSLambda_FullAccess** IAM Policy.

### GitHub

#### Workflow

* This workflow is triggered when a change is pushed to master.
* The code change is then deployed to Lambda. The change doesn't trigger a test.

#### Secrets

* For GitHub Actions to properly work you need to define the following secrets:

| Secret                | Description                                                                   |
| --------------------- | ----------------------------------------------------------------------------- |
| AWS_ACCESS_KEY_ID     | Get this from your IAM User. Used to connect to AWS.                          |
| AWS_SECRET_ACCESS_KEY | Get this from your IAM User. Used to connect to AWS.                          |
| AWS_DEFAULT_REGION    | The AWS Region you're using. Used to connect to AWS.                          |
| LAMBDA_FUNCTION_NAME  | The AWS Lambda Function name you'll be using. Function to deploy code to.     |
| LAMBDA_LAYER_ARN      | The GitHub Action will install the function dependencies as a separate layer. |

### Environment Variables

| Variable          | Description                                                                      | Example     |
| ----------------- | -------------------------------------------------------------------------------- | ----------- |
| REGION            | AWS Region used.                                                                 | us-east-1   |
| SENDER            | Email address that SES will use to send the mail.                                | foo@bar.com |
| RECIPIENT         | Email address that SES will send the email to.                                   | foo@bar.com |
| UNITS_SIMFONIA    | The units you currently hold on Simfonia. Use the app to find this information.  | 123.456     |
| UNITS_DIVERSO     | The units you currently hold on Diverso A. Use the app to find this information. | 123.456     |
| INVESTED_SIMFONIA | Amount of money you currently invested in Simfonia.                              | 123         |
| INVESTED_DIVERSO  | Amount of money you currently invested in Diverso.                               | 123         |

## How it works

* BRD Asset Management exposes a JSON containing the information about each portfolio (example for [Simfonia](https://www.brdam.ro/assets/json/istorics.json))
* I used this to fetch the data and based on the number of units you own and the total investment you made, it uses Jinja to render an HTML template which is then sent to you email address using AWS SES.

## Development

### Requirements

* Python 3.6.x
* Install python requirements:
  
```bash
pip install -r requirements.txt
```

### Local run

* Running locally will open a new tab in Firefox with the HTML template. No email is sent when you run on local. Example run:
```bash
SENDER="BRD Asset Manager <email@foo.com>" RECIPIENT="foo.bar@baz.com" UNITS_SIMFONIA="123.45" INVESTED_SIMFONIA="12345" UNITS_DIVERSO="678.9" INVESTED_DIVERSO="123123" python main.py
```
