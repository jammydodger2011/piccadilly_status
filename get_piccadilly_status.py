import json
import requests
import os

def get_piccadilly_status():

    try:
        response = requests.get('https://api.tfl.gov.uk/Line/piccadilly/Status')
        status_code = response.status_code
        data = response.json()
        line_status = data[0]['lineStatuses'][0]

        status_severity = line_status['statusSeverity']
        status_description = line_status['statusSeverityDescription']

        print(status_severity)
        print(status_description)

        message = {'severity': status_severity,
                'description': status_description}
        
    except:
        message = "Couldn't reach TFL"
        status_code = 500

    return {'body': message, 'code': status_code}