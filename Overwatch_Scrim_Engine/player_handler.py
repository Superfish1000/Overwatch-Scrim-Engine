from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

API_URL = ['https://www.googleapis.com/auth/spreadsheets.readonly']

PLAYER_SPREADSHEET = '1iUS8gWn3RaZbiyUWkToArjh4x0a_owWgRmvERtict9M'
SHEET_RANGE_NAME =  'Form Responses 1!A1:E'

def getPlayers():
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', API_URL)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Load the sheets API
    sheet = service.spreadsheets()
    player_spreadsheet = sheet.values().get(spreadsheetId=PLAYER_SPREADSHEET,
                                range=SHEET_RANGE_NAME, ).execute()
    player_data = player_spreadsheet.get('values', [])

    if not values:
        print("No player data in sheet.")
        return None
    return values
