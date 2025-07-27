import gspread


class Sheets:
    def __init__(self, service_file_path: str, sheet_id: str):
        self.client = gspread.service_account(service_file_path)
        self.spreadsheet = self.client.open_by_key(sheet_id)
        self.worksheets = self.spreadsheet.worksheets()

    def update_sheets(self):
        self.worksheets = self.spreadsheet.worksheets()
        return self.worksheets

    def add_row(self, ws_index: int, row_data: dict):
        self.worksheets[ws_index].append_row(row_data)

