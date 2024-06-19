from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta

creds = Credentials.from_authorized_user_file("/Users/isabelmelo/Desktop/resoulse/credentials/client_secret copy.json")

service = build('calendar', 'v3', credentials=creds)

start_time = datetime.now(timezone.utc)
end_time = start_time + timedelta(days=7)
time_min = start_time.isoformat()
time_max = end_time.isoformat()
while(1):
    userId = input("please enter your user id: ")
    freebusy_query = {
        'timeMin': time_min,
        'timeMax': time_max,
        'timeZone': 'UTC',
        'items': [{'id': userId}]
    }

    try:
        freebusy_result = service.freebusy().query(body=freebusy_query).execute()
    except HttpError as error:
        print(f'An error occurred: {error}')
        freebusy_result = None

    if freebusy_result is None:
        print('No free/busy information available.')
    else:
        for cal_id, cal_data in freebusy_result['calendars'].items():
            print(f'Free/busy information for calendar {cal_id}:')
            for busy in cal_data['busy']:
                start_time = busy['start']
                end_time = busy['end']
                print(f'{start_time} to {end_time}')
