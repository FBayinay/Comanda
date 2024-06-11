class DataEntryLogic:
    def __init__(self, column_names):
        self.column_names = column_names
        self.data = {}

    def enter_data(self, column_index, data):
        column_name = self.column_names[column_index]
        self.data[column_name] = data

    def validate_data(self):
        # Verifica que todos los campos, excepto el primero (autoincremental), estén completos
        for column_name in self.column_names[1:]:
            if column_name not in self.data or not self.data[column_name]:
                return False
        return True

    def get_entered_data(self):
        return self.data
