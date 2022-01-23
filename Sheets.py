import httplib2
import apiclient
import json
import os
from oauth2client.service_account import ServiceAccountCredentials


def create_keyfile_dict():
    variables_keys = {
        "type": "service_account",
        "project_id": "discordcinema",
        "private_key_id": "0865928fc3297d430b5d499f39b341f56c759938",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCZIF0VRkkdznyS\noU1MoXnZn+JgrRgT3CP/J6XwFrnc8FSHqqvcL/4qWgZNw5yrNWvZ9IhRc4rbc2n5\nQv0q+QRGNq4hPYdqpHO/5X0rf+mWkbizoeQgGDXG7Ym/REuIxjTH3OfL5OYct8t0\nKkFqs1BYl5gTHsuptNrqpTnhNmkKey1yxVb63qAFPFzgvThNEcAegGd4Rh8syaGA\nlvIqVjuH2oMcNndR3rj/3VgsmHvu69NGuZUbM+Lt4JyySMxTh0ivKUtCefuR+XpA\nuJlGh+CkM0+CvYYgfzkWbGax8wbY4YOGRxCVtxO9ph/IdfTf3SL7eR3Gc7HyaO7Y\nfvf7dhx9AgMBAAECggEAB378V42GiElCs2nmjxULkkH/ssRefKBm+bdu6eMu65gv\nRyntely2GEwqaVWlXoNBuZx9LOGXX1lVy4BCRP+GPEqyeQmaTrfou7DoEQBUxsxw\n6ohHEuQkg82+k8ir2vD7Bfq0NTjKJAdCVDg6VhcbnI6lQPBdv3vNSLXYcMQ5Xawp\nDjYIAqUfo4xoMBDtz32Vav+I4mgnIm4ohvihyaobUNn+17wKgJqePDcgI+Yt+xC+\ny0hoI23PMaV3uP4Er5pZm0KP/qbKLLKnnNvNYDXnUV1azoSzed10NQl1KqEewRHc\nRt2ud9ypg0jt1BIaXFLvP/WpPjIQELw0fiZjVIASsQKBgQDYS+sXsaWNStCTbNrr\nUSsF0Xw84qSOPM87uae+mmAgBVyWBSIOjtQ1KTDAaybhCecL1jQVjx5HSPpl1efF\nT14/1YbhICGWRkKObfWCtlWeJhvXugCiuxjSC4zzFPbXVSz0p1kSRnFlLTYNkFK+\nA48+lS8b6wgqyORKR4ce/aiPrQKBgQC1O/230jgSscyyu7/W5Rar5DXT5IZVQ70e\nc1tr9AgkfWuJulkc9zeIJAu9Mnd/3Vw+q35NltIm7bf2ygwIQ2oR9TW25i168OHi\ntKqcy9H8VPvdiC8DtR690clunn+OZQkDO5L7NtMlrmzUmSIK9afBLcgqcaX02wTV\niBm96QEaEQKBgH9DK++k9mNLwaz8P1J1T3r85rxsHaYS4VuiwK/E5QnyHaenHYKz\nRuiAc87DPPzrdqXgQoTs0EPhDHMeiF/vcuTcHaAX56sja8WhrPJblcSXZ4pmRjl5\nHAF6ClR74UCRPQI19JJsIAwHreYNJKHoNj/8RtuGTifeS3Po4fe6B5OBAoGAaZ7m\nxKR9DVgVheypZuHoDpFXVYAPUc3Cf+aW1xlHTYzSiVfS63CgKnVnagHpZtlpExT6\n7NkC7LEJz4f87yvqu0B+53LJ+qY73tWPwQWAAWC90GO3kp+RpOqITDGPATucvweP\nJ1zSPVmkD1qXXm/ALnMx/ppxL3wdGxzQc79BZyECgYB7zBmD6rucjXScPkWhL6lP\nPEUGU0rY2/GDs0QPTa59xnCmzQSnXpQDu2010R86FC/iRGz3/PSpMlN9oO8Xu1oU\nMbE1jvSgh2xp6I0K1ksVr7lMmEhPRnEa2MAHxKsiznVX++NiD4rK7AfUQOghzoTU\nk6hQvrqf4z8o80/Kyubv+g==\n-----END PRIVATE KEY-----\n",
        "client_email": "discordbotaccount@discordcinema.iam.gserviceaccount.com",
        "client_id": "106613120822277941337",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/discordbotaccount%40discordcinema.iam.gserviceaccount.com"
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
