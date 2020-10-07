#---------------FILE OVERVIEW--------------------------------
#CONTAINS FUNCTIONS THAT HELP WITH WRITING TO GOOGLE SHEETS
#------------------------------------------------------------
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope) #requires creds
# client = gspread.authorize(creds)

# def writeToSheet(book, sheet, header, data, sheet_range):
#     if len(data) > 0:
#         #sheet_range ="!A1:L10000"
#         client.login()
#         book = client.open(book)
#         s = book.worksheet(sheet)
#         book.values_clear(sheet + sheet_range) #clears range
#         data.insert(0, header)
#         cells = []
#         for row_num, row in enumerate(data):
#             for col_num, cell in enumerate(row):
#                 cells.append(gspread.Cell(row_num + 1, col_num + 1, data[row_num][col_num]))
#         s.update_cells(cells)

# def getSheetData(book, sheet):
#     s = client.open(book).worksheet(sheet)
#     data = s.get_all_records()
#     return data