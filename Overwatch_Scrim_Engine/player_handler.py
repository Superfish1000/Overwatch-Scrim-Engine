from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

API_URL = ['https://www.googleapis.com/auth/spreadsheets.readonly']

PLAYER_SPREADSHEET = '1iUS8gWn3RaZbiyUWkToArjh4x0a_owWgRmvERtict9M'
# Start the range at A2 so that we remove the first line with the ident field.  Range is Line 2+, A-E
SHEET_RANGE_NAME =  'Form Responses 1!A2:E' 

# ############### TODO ###############
# Add check for credentials.json file that allows user to upload the required API file
# This would be a good thing to do in browser for usability.
# Currently, if the credentials.json file is not found in the root the system will error.

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
            creds = flow.run_local_server(port=0) # Launch browser on bad pickel?
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Load the sheets API
    sheet = service.spreadsheets()
    player_spreadsheet = sheet.values().get(spreadsheetId=PLAYER_SPREADSHEET,
                                range=SHEET_RANGE_NAME, ).execute()
    player_data = player_spreadsheet.get('values', [])

    if not player_data:
        print("No player data in sheet.")
        return None
    return player_data

# This function is to return a list of palyer battle.net names.
def extractBattleNet(playerDict):
    battleNetIDs = []
    for battleNet in playerDict:
        battleNetIDs.append(battleNet[1])
    return battleNetIDs

# This function is to return a list of palyer Discord names.
def extractDiscord(playerDict):
    discordIDs = []
    for discordID in playerDict:
        discordIDs.append(discordID)
    return discordIDs

# Returns a battle.net or Discord ID formatted using '-' instead of '#' for URL compatibility reasons.
def formatForWeb(battleNet):
    return battleNet.replace("#", "-")

def formatAllForWeb(playerDict):
    formatted = []
    for ID in playerDict:
        formatted.append(formatForWeb(ID))
    return formatted
