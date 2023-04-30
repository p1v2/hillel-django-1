from django.db.models import Avg
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

from books.models import Book, Author

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1v_feqQAiR6ZVihIbwL1I51mA_WxJbhAuTZKnYwHGNi8'
BOOKS_RANGE_NAME = 'Books!A2:E'
AUTHORS_RANGE_NAME = 'Authors!A2:E'


def get_service(user):
    # Get django all auth credentials for Google Sheets
    credentials = Credentials(
        token=user.socialaccount_set.get(provider="google").socialtoken_set.get().token,
        refresh_token=user.socialaccount_set.get(provider="google").socialtoken_set.get().token_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    # Getting credentials from service account file
    # credentials = service_account.Credentials.from_service_account_file("service_account.json")

    service = build('sheets', 'v4', credentials=credentials)
    return service


def read_from_google_sheets(user):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # Getting credentials from service account file
    service = get_service(user)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=BOOKS_RANGE_NAME).execute()
    values = result.get('values', [])
    print(values)

    # Batch read
    # result = sheet.values().batchGet(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #                                     ranges=[
    #                                         BOOKS_RANGE_NAME,
    #                                         AUTHORS_RANGE_NAME
    #                                     ]
    #
    #                                     ).execute()
    # print(result)


def write_to_google_sheets(user, books: [Book], authors: [Author]):
    # Getting credentials from service account file
    service = get_service(user)

    # Call the Sheets API
    sheet = service.spreadsheets()

    books_values = [
        [book.name, book.price, book.count_sold, book.authors_string, book.country and book.country.name]
        for book in books
    ]
    authors_values = [
        [author.first_name, author.last_name, author.starred, author.books.count(), author.books.aggregate(Avg("price"))["price__avg"]]
        for author in authors
    ]

    # Single update
    # result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #                                range=SAMPLE_RANGE_NAME,
    #                                valueInputOption="USER_ENTERED",
    #                                body={"values": values}
    #                                ).execute()

    # Batch clear before update
    result = sheet.values().batchClear(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                       body={
                                           "ranges": [
                                               BOOKS_RANGE_NAME,
                                               AUTHORS_RANGE_NAME
                                           ]
                                       }
                                       ).execute()


    # Batch update
    result = sheet.values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        body={
                                            "valueInputOption": "USER_ENTERED",
                                            "data": [
                                                {
                                                    "range": BOOKS_RANGE_NAME,
                                                    "majorDimension": "ROWS",
                                                    "values": books_values
                                                },
                                                {
                                                    "range": AUTHORS_RANGE_NAME,
                                                    "majorDimension": "ROWS",
                                                    "values": authors_values
                                                }
                                            ]
                                        }
                                        ).execute()

    print(result)
