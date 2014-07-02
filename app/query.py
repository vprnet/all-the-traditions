#!/usr/bin/python
from google_spreadsheet.api import SpreadsheetAPI
from datetime import datetime
from config import GOOGLE_SPREADSHEET


def get_google_sheet(sheet_key=False, sheet_id='od6'):
    """Uses python_google_spreadsheet API to interact with sheet"""
    api = SpreadsheetAPI(GOOGLE_SPREADSHEET['USER'],
        GOOGLE_SPREADSHEET['PASSWORD'],
        GOOGLE_SPREADSHEET['SOURCE'])
    sheet = api.get_worksheet(sheet_key, sheet_id)
    sheet_object = sheet.get_rows()
    return sheet_object


def get_concerts():
    """Get all concerts from the Google Drive doc"""
    concerts = get_google_sheet('tVMaafzEd2pVoKriuwjgdQw')
    for concert in concerts:
        date = datetime.strptime(concert['date'], '%m/%d/%Y')
        time = datetime.strptime(concert['time'], '%H:%M:%S')
        weekday_month = date.strftime('%A, %B')
        number = date.strftime('%d').lstrip('0')
        concert['date'] = weekday_month + ' ' + number
        concert['time'] = time.strftime('%I:%M %p').lstrip('0')

    return concerts
