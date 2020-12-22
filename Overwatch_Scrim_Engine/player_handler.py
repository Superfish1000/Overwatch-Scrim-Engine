from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

PLAYER_SPREADSHEET = '1iUS8gWn3RaZbiyUWkToArjh4x0a_owWgRmvERtict9M'
# Start the range at A2 so that we remove the first line with the ident field.  Range is Line 2+, A-E.
SHEET_RANGE_NAME =  'Form Responses 1!A2:E' 

# To call get players, creds data must be passed in to be used for the GSuite API.
def getPlayers(creds):

    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)

    # Load the sheets API.
    sheet = service.spreadsheets()
    player_spreadsheet = sheet.values().get(spreadsheetId=PLAYER_SPREADSHEET, range=SHEET_RANGE_NAME, ).execute()
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

# Uses the formatForWeb function in a loop to format all user handles in a list for web compatibility.
def formatAllForWeb(playerDict):
    formatted = []
    for ID in playerDict:
        formatted.append(formatForWeb(ID))
    return formatted
