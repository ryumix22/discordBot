import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'discordcinema-0865928fc329.json'
spreadsheets_id = '1UeX3KFw_7Ed5zosY1cBok2fX5iSui13-VIYwjG-qzmY'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

# values = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheets_id,
#         range='A4:A30',
#         majorDimension='COLUMNS'
#     ).execute()
#
# print(values.get('values')[0])


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
