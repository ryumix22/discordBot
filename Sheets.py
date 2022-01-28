import httplib2
import apiclient
import os
from oauth2client.service_account import ServiceAccountCredentials


def create_keyfile_dict():
    variables_keys = {
        "type": "service_account",
        "project_id": "botdiscord-339615",
        "private_key_id": os.getenv('KEY'),
        "private_key": os.environ.get('PKEY').replace('\\n', '\r\n'),
        "client_email": "botdisc@botdiscord-339615.iam.gserviceaccount.com",
        "client_id": "112888256103414069059",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/botdisc%40botdiscord-339615.iam.gserviceaccount.com"
    }
    return variables_keys


spreadsheets_id = '1UeX3KFw_7Ed5zosY1cBok2fX5iSui13-VIYwjG-qzmY'

credentials = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(),
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

# values = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheets_id,
#         range='A4:F47',
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


def getRangeByRows(startName: str, startIndex, endName:str, endIndex):
    tableRange = startName + str(startIndex) + ':' + endName + str(endIndex)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheets_id,
        range=tableRange,
        majorDimension='ROWS'
    ).execute()
    return values.get('values')


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
