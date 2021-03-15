from PyQt5.QtWidgets import QWidget, QApplication, QListWidget, QPushButton, QListWidgetItem, QMessageBox, QLineEdit
import project1
import sqlite3
from typing import Tuple


class Window(QWidget):
    def __init__(self, data_to_show):
        super().__init__()
        self.data = data_to_show
        self.list_control = None
        self.setup_window()

    def open_db(self,filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        db_connection = sqlite3.connect(filename)
        cursor = db_connection.cursor()
        return db_connection, cursor

    def close_db(self,connection: sqlite3.Connection):
        connection.commit()
        connection.close()

    def setup_window(self):
        self.setWindowTitle("Project 1 GUI and Data Visualization")
        display_list = QListWidget(self)
        self.list_control = display_list
        self.put_data_in_list(self.data)
        display_list.resize(500, 400)
        self.setGeometry(500, 100, 400, 500)
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(QApplication.instance().quit)
        exit_button.resize(exit_button.sizeHint())
        exit_button.move(300, 450)
        sort_descending_button = QPushButton("Sort Descending", self)
        sort_descending_button.move(100, 450)
        sort_descending_button.clicked.connect(self.sort_data_descending)
        update_data_button = QPushButton("Update Data", self)
        update_data_button.move(100, 400)
        update_data_button.clicked.connect(self.update_data)
        run_visual_button = QPushButton("Run Visualization", self)
        run_visual_button.move(200, 400)
        run_visual_button.clicked.connect(self.display_visualization_collegegrad)
        self.show()

    def put_data_in_list(self, data):
        locations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                     "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                     "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                     "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                     "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        for item,state in zip(data,locations):
            display_text = f"{item} in state: {state}"
            list_item = QListWidgetItem(display_text, self.list_control)

    def update_data(self):
        message = QMessageBox(self)
        message.setText("Please wait while we update data")
        message.setWindowTitle("Updating Data...")
        message.show()
        project1.main()

    def display_visualization_collegegrad(self, cursor):
        visual_message = QMessageBox(self)
        visual_message.setText("Displaying...")
        visual_message.setWindowTitle("Visualization")
        project1.show_figure_collegegrad_vs_job(cursor)
        visual_message.show()

    def sort_data_descending(self, data):
        locations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                     "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                     "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                     "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                     "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        data.reverse()
        locations.reverse()
        for item,state in zip(data, locations):
            display_text = f"{item} in state: {state}"
            list_item = QListWidgetItem(display_text, self.list_control)
