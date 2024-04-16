from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import Config

import os
import sys

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import threading

Config.set('graphics', 'fullscreen', 'auto')

class ComandaApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_data = None
        self.table_num = None

    def build(self):
        self.table_buttons_layout = GridLayout(cols=20, spacing=10, size_hint_y=None)
        self.table_buttons_layout.bind(minimum_height=self.table_buttons_layout.setter('height'))
        self.populate_table_buttons()

        self.data_layout = BoxLayout(orientation='vertical', padding=10)
        self.data_label = Label(text='Seleccione una mesa para ver los datos', size_hint=(1, 0.1))
        self.data_scrollview = ScrollView(size_hint=(1, 0.9))
        self.data_container = GridLayout(cols=8, spacing=10, size_hint_y=None)
        self.data_container.bind(minimum_height=self.data_container.setter('height'))
        self.data_scrollview.add_widget(self.data_container)
        self.data_layout.add_widget(self.data_label)
        self.data_layout.add_widget(self.data_scrollview)

        self.exit_button = Button(text='Salir', size_hint=(1, None), height=50)
        self.exit_button.bind(on_press=self.exit_app)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.table_buttons_layout)
        main_layout.add_widget(self.data_layout)
        main_layout.add_widget(self.exit_button)

        Clock.schedule_interval(self.update_data, 7)

        return main_layout

    def populate_table_buttons(self):
        self.table_buttons_layout.clear_widgets()
        for i in range(20):
            table_button = Button(text=f'Mesa {i+1}', size_hint=(None, None), width=87, height=50)
            table_button.bind(on_press=lambda instance, table_num=i+1: self.show_table_data(table_num))
            self.table_buttons_layout.add_widget(table_button)

            reset_button = Button(text='Reset', size_hint=(None, None), width=87, height=50)
            reset_button.bind(on_press=lambda instance, table_num=i+1: self.reset_table(table_num))
            self.table_buttons_layout.add_widget(reset_button)

    def show_table_data(self, table_num):
        threading.Thread(target=self.update_table_data, args=(table_num,)).start()

    def update_table_data(self, table_num):
        new_data = self.get_product_data(table_num)
        if new_data != self.product_data:
            self.product_data = new_data
            Clock.schedule_once(lambda dt: self.update_ui(table_num), 0)

    def update_ui(self, table_num):
        self.data_label.text = f'Datos de la Mesa {table_num}'
        self.data_container.clear_widgets()
        for row_index, row in enumerate(self.product_data):
            if not row:
                continue

            cell_value = row[2]
            if not cell_value.lower() == "si":
                for col_index, item in enumerate(row):
                    data_box = Label(text=str(item), size_hint=(None, None), width=200, height=50)
                    self.data_container.add_widget(data_box)
                none = Label(text=str(' '), size_hint=(None, None), width=50, height=50)
                none2 = Label(text=str(' '), size_hint=(None, None), width=50, height=50)
                self.data_container.add_widget(none)
                self.data_container.add_widget(none2)

            elif cell_value is not None and cell_value.lower() == "si":
                for col_index, item in enumerate(row):
                    data_box = Label(text=str(item), size_hint=(None, None), width=200, height=50)
                    self.data_container.add_widget(data_box)

                btn_minus = Button(text='-', size_hint=(None, None), width=50, height=50) 
                btn_plus = Button(text='+', size_hint=(None, None), width=50, height=50)

                btn_minus.bind(on_press=lambda instance, row_index=row_index: self.update_quantity(table_num, row_index, -1))
                btn_plus.bind(on_press=lambda instance, row_index=row_index: self.update_quantity(table_num, row_index, 1))

                self.data_container.add_widget(btn_minus)
                self.data_container.add_widget(btn_plus)

        self.table_num = table_num

    def exit_app(self, instance):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def get_product_data(self, table_num):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        spreadsheet_id = '1PH9IOkykSvm4QcBt7ulv7q4qK9eBQ5PcHzpBWffm30Q'
        sheet_name = f'Mesa {table_num}'
        
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        data = sheet.get_all_values()

        return data

    def update_data(self, dt):
        threading.Thread(target=self.update_general_data).start()

    def update_general_data(self):
        new_data = self.get_product_data(self.table_num)
        if new_data != self.product_data:
            self.product_data = new_data
            Clock.schedule_once(lambda dt: self.update_ui(self.table_num), 0)

    def update_quantity(self, table_num, row_index, change):
        threading.Thread(target=self.threaded_update_quantity, args=(table_num, row_index, change)).start()

    def threaded_update_quantity(self, table_num, row_index, change):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
    
        spreadsheet_id = '1PH9IOkykSvm4QcBt7ulv7q4qK9eBQ5PcHzpBWffm30Q'

        sheet = client.open_by_key(spreadsheet_id).worksheet(f'Mesa {table_num}')
        cell_value = sheet.cell(row_index + 1, 4).value
        if cell_value is None:
            current_value = 0
        else:
            current_value = int(cell_value)
        new_value = current_value + change
        sheet.update_cell(row_index + 1, 4, str(new_value))

    def reset_table(self, table_num):
        threading.Thread(target=self.threaded_reset_table, args=(table_num,)).start()

    def threaded_reset_table(self, table_num):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
    
        spreadsheet_id = '1PH9IOkykSvm4QcBt7ulv7q4qK9eBQ5PcHzpBWffm30Q'

        sheet = client.open_by_key(spreadsheet_id).worksheet(f'Mesa {table_num}')
        columna_datos = sheet.col_values(2)
        numero_datos = len([dato for dato in columna_datos if dato.strip()])  # Contar celdas no vacías
        cell_list = sheet.range(f'D2:D{numero_datos}')
        for cell in cell_list:
            print("El valor de la celda es:",cell.value)
            if  cell.value=='':
                pass
            else:
                cell.value = '0'
        sheet.update_cells(cell_list)
        self.show_table_data(table_num)

if __name__ == '__main__':
    ComandaApp().run()
