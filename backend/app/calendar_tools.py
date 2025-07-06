import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from dateutil import parser
from langchain_core.tools import tool

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'key.json'
CALENDAR_ID = os.getenv("CALENDAR_ID")

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)


@tool
def check_calendar_availability(day: str) -> list:
    """
    Checks the Google Calendar for available time slots on a given day.
    Use this to check for open time slots on a specific day. It can understand dates like 'tomorrow', 'July 7th, 2025', or '2025-07-07'.
    """
    try:
        date = parser.parse(day).date()
    except (ValueError, parser.ParserError):
        return "Invalid date format. Please provide a clear date like 'tomorrow', 'October 31st', or '2024-10-31'."

    start_of_day = datetime.combine(date, datetime.min.time()).isoformat() + 'Z'
    end_of_day = datetime.combine(date, datetime.max.time()).isoformat() + 'Z'

    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=start_of_day,
                                        timeMax=end_of_day, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return [f"The entire day of {date.strftime('%A, %B %d, %Y')} is free."]

    busy_slots = []
    for event in events:
        start = parser.parse(event['start'].get('dateTime', event['start'].get('date')))
        end = parser.parse(event['end'].get('dateTime', event['end'].get('date')))
        busy_slots.append((start, end))

    return [f"Busy from {start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')}" for start, end in busy_slots]


@tool
def book_appointment(start_time_str: str, end_time_str: str, summary: str) -> str:
    """
    Use this to book an appointment once the user has confirmed the time.
    You must provide a summary, a start time, and an end time.
    The times must include the full date and time, e.g., 'July 7th 2025 at 4pm'.
    """
    try:
        start_time = parser.parse(start_time_str)
        end_time = parser.parse(end_time_str)
    except (ValueError, parser.ParserError):
         return "Invalid start or end time format. Please provide a clear date and time."

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    try:
        event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return f'Success! Appointment "{summary}" created. View it here: {event.get("htmlLink")}'
    except Exception as e:
        return f"An error occurred while booking: {e}"
