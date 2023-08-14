import json
import requests
import os
from datetime import datetime
import pytz
from get_piccadilly_status import get_piccadilly_status

print('Starting...')
if os.getenv('PLATFORM') == 'docker':
    environment = 'docker'
    print('Running in Docker')
else:
    environment = 'lambda'
    print('Running in Lambda')
    print("Importing boto3...")
    import boto3
    print("Connecting to ses...")
    ses = boto3.client('ses', region_name='eu-west-1')

print("Platform is ", os.getenv('PLATFORM'))

def lambda_handler(event, context):

    """
    Gets piccadilly line status.
    """

    # Define email source and destinations
    source_email = ''
    dest_emails = []

    # Get the British time zone
    london_tz = pytz.timezone('Europe/London')
    current_time_utc = datetime.now(pytz.utc)
    current_time_bst = current_time_utc.astimezone(london_tz)

    # Format the British time
    current_time_formatted = current_time_bst.strftime('%H:%M %dth %b %Y')

    # Call helper file to bring back piccadilly status
    piccadilly_status = get_piccadilly_status()
    print(piccadilly_status)

    # Create the email subject and body
    email_subject = "🚇 Piccadilly Line: " + piccadilly_status['body']['description'] + "! 🚇"
    email_body = (
        "Hi commuter!\n\n"
        f"The Piccadilly Line status is: {piccadilly_status['body']['description']} as of {current_time_formatted}. "
        "Please keep up to date with the line's status if you're planning to travel in the near-future.\n\n"
        "Happy commuting!\n"
        "James' Piccadilly Line status scraper"
    )
    

    if environment == 'lambda' and piccadilly_status['body']['severity'] != 5:
        # Send the email
        response = ses.send_email(
            Source=source_email,
            Destination={
                'ToAddresses': dest_emails
            },
            Message={
                'Subject': {'Data': email_subject},
                'Body': {'Text': {'Data': email_body}}
            }
        )
        print("Email sent:", response)
    else:
        if environment != 'lambda':
            print("Not sending email as environment is not lambda.")
        else:
            print("No email sent. Severity code is ", 
                  piccadilly_status['body']['severity'], 
                  "and Piccadilly has ", 
                  piccadilly_status['body']['description'])

    return {
        'statusCode': 200,
        'body': json.dumps(piccadilly_status)
    }

if environment != 'lambda':
    lambda_handler(1,1)

print('...Finished')

