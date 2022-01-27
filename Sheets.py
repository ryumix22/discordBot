import httplib2
import apiclient
import json
import os
from oauth2client.service_account import ServiceAccountCredentials


def create_keyfile_dict():
    variables_keys = {
        
    }
    return variables_keys

# client_secret = os.environ.get('GOOGLE_CREDENTIALS')  # This pulls your variable out of Config Var and makes it available
# if client_secret is None:  # This is to detect if you're working locally and the Config Var therefore isn't available
#     print('\n\nResorted to local JSON file.\n\n')
#     with open('google-credentials.json') as json_file: # ... so it pulls from the locally stored JSON file.
#         client_secret = json.load(json_file)
# else:
# client_secret = json.loads(client_secret) # This converts the Config Var to JSON for OAuth

# CREDENTIALS_FILE = 'google-credentials.json'


spreadsheets_id = '1UeX3KFw_7Ed5zosY1cBok2fX5iSui13-VIYwjG-qzmY'

credentials = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(),
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

# values = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheets_id,
#         range='A4:A39',
#         majorDimension='ROWS'
#     ).execute()
#
# print(values.get('values'))

# values = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheets_id,
#         range='A37:F37',
#         majorDimension='ROWS'
#     ).execute()
#
# print(values.get('values'))


def getLastColumn():
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheets_id,
        range='A:A',
        majorDimension='COLUMNS'
    ).execute()
    return len(values.get('values')[0])


def getLastRow():
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheets_id,
        range='3:3',
        majorDimension='ROWS'
    ).execute()
    return len(values.get('values')[0])


def getColumnValues(columnName: str, startIndex, endIndex):
    tableRange = columnName + str(startIndex) + ':' + columnName + str(endIndex)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheets_id,
        range=tableRange,
        majorDimension='COLUMNS'
    ).execute()
    return values.get('values')[0]


def getRowsValues(startRowName: str, endRowName: str, index):
    tableRange = startRowName + str(index) + ':' + endRowName + str(index)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheets_id,
        range=tableRange,
        majorDimension='ROWS'
    ).execute()
    if values.get('values') is not None:
        return values.get('values')[0]


def setCellValue(cell: str, value: str):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheets_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": cell,
                    "majorDimension": "ROWS",
                    "values": [[value]]
                }
            ]
        }
    ).execute()
