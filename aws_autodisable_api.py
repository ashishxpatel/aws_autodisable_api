import json
import boto3
from botocore.vendored import requests

SLACK_URL = ""

# Function to disable access key so it can no longer be used

def disable_access(accessKey, userName, country):
    notifier = ""
    # Create IAM client
    iam = boto3.client("iam")

    # Update access key to be active
    try:
        iam.update_access_key(
            AccessKeyId=accessKey, Status="Inactive", UserName=userName
        )
        notifier += (
            "*Unauthorized AWS Access Key usage identified :scream:, disabled for: * "
            + accessKey
            + " "
            + userName
            + " *from* "
            + country
        )
    except:
        notifier += (
            "*I was not able to disable the key for you, please check out the console*"
        )
    send_message(notifier)


# Template function to send notifications to Slack


def send_message(message):
    payload = {"text": message}
    try:
        return requests.post(
            url=SLACK_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as e:
        print(e.message)
        return False


# Main lambda function to call the rest and execute your code


def lambda_handler(event, context):
    access_info = []
    user_key_id = event["Records"][0]["Sns"]["Message"]
    user_key_message_json = json.loads(user_key_id)
    identity_information = user_key_message_json["message"]
    accessKey, userName, country = identity_information.split()
    disable_access(accessKey, userName, country)