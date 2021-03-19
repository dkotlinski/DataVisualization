from PyQt5.QtWidgets import *
import project1


class FirstWindow(QWidget):
    def __init__(self, data_to_show, cursor):
        super().__init__()
        self.cursor = cursor
        self.data = data_to_show
        self.list_control = None
        self.setup_window()

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
        update_data_button.clicked.connect(self.get_file_update)
        run_visual_button = QPushButton("Run Visualization", self)
        run_visual_button.move(200, 400)
        run_visual_button.clicked.connect(self.show_new_window)
        self.show()

    def show_new_window(self):
        self.w = SecondWindow(self.cursor)
        self.w.show()

    def get_file_update(self):
        ourfilter = "Excel Files (*.xls *.xlsx *.xlsm)"
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter(ourfilter)
        if dialog.exec_():
            filename = dialog.selectFiles
            return filename

    def put_data_in_list(self, data):
        locations = project1.state_abbrev()
        for item, state in zip(data, locations):
            display_text = f"{item} in state: {state}"
            list_item = QListWidgetItem(display_text, self.list_control)

    def sort_data_descending(self, data):
        locations = project1.state_abbrev()
        data.reverse()
        locations.reverse()
        for item, state in zip(data, locations):
            display_text = f"{item} in state: {state}"
            list_item = QListWidgetItem(display_text, self.list_control)


class SecondWindow(QWidget):
    def __init__(self, cursor):
        super(SecondWindow, self).__init__()
        self.setup(cursor)

    def setup(self, cursor):
        self.setGeometry(500, 100, 400, 500)
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(QApplication.instance().quit)
        exit_button.resize(exit_button.sizeHint())
        exit_button.move(300, 450)
        college_button = QPushButton("College Grad Data", self)
        college_button.move(30, 450)
        college_button.clicked.connect(project1.show_figure_collegegrad_vs_job(cursor))
        loan_button = QPushButton("Loan Data", self)
        loan_button.move(200, 450)
        loan_button.clicked.connect(project1.show_figure_declining_balance(cursor))
        self.show()

