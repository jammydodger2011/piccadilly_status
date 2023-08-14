import json
import requests
from datetime import datetime
import pandas as pd
import time

def lambda_handler(event, context):

    now = datetime.now()

    # --------------------------- Find next piccadilly line trains ---------------------------
    picc_url = 'https://api.tfl.gov.uk/Line/piccadilly/Arrivals/940GZZLUBDS?direction=inbound'
    response = requests.get(picc_url)

    # create a formatted string of the Python JSON object
    df = pd.DataFrame(response.json())

    # find next train
    next_train = (df[['expectedArrival','currentLocation','timeToStation']])
    arrival_time = pd.DataFrame(columns = ['Arrival'])
    arrival_time['Arrival'] = pd.to_datetime(next_train['expectedArrival'], format = "%Y-%m-%dT%H:%M:%S", utc = True)
    next_train = pd.concat([next_train,arrival_time], axis = 1)

    # Sort arrivals
    next_train_sorted = next_train.sort_values("timeToStation")

    return next_train_sorted

if __name__ == "__main__":
    # For local testing, provide mock values for event and context.
    # You can adjust the event data based on your Lambda function's expected input.
    event = {
        1
    }
    
    context = {
        1
    }

    # Call the Lambda handler function with the provided event and context
    result = lambda_handler(event, context)
    print(result)