# comanda/database/data_entry_logic.py

class DataEntryLogic:
    def __init__(self, table_name):
        self.table_name = table_name
        self.data = {}

    def enter_data(self, column_index, data):
        column_name = self.column_names[column_index]
        self.data[column_name] = data

    def validate_data(self):
        for column_name in self.column_names[1:]:
            if column_name not in self.data or not self.data[column_name]:
                return False
        return True

    def get_entered_data(self):
        return self.data
