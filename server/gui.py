from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import *
import sys
import math
import threading
import time

from server import Server

class Updates(QThread):
    is_active = False
    _signal = pyqtSignal(str)
    _msg_queue = []
    def __init__(self):
        super(Updates, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        is_active = True
        while is_active or _msg_queue:
            if not self._msg_queue:
                time.sleep(0.1)
                continue
            msg = self._msg_queue.pop(0)
            self._signal.emit(msg)

    def msger(self, msg:str):
        self._msg_queue.append(msg)

class Updates(QThread):
    is_active = False
    _signal = pyqtSignal(int, str)
    _msg_queue = []
    def __init__(self):
        super(Updates, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        is_active = True
        while is_active or _msg_queue:
            if not self._msg_queue:
                time.sleep(0.1)
                continue
            msg = self._msg_queue.pop(0)
            self._signal.emit(msg[0], msg[1])

    def msger(self, sid:int, msg:str):
        self._msg_queue.append((sid, msg))

class PyQtGUI(QWidget):
    _progress_bar = None
    _thread = None
    _is_working = False
    _flag_init = False

    slave_workers = []

    def __init__(self):
        super().__init__()
        self._thread = Updates()
        self._thread._signal.connect(self.msg_listener)

        self._server = Server(self.update_listener, self._thread.msger)

        self.initUI()
    
    def closeEvent(self, event):
        self._server.stop()
        event.accept()

    def msg_listener(self, slave_id, msg):
        if msg == 'new':
            new_slave = dict()
            new_slave['id'] = slave_id
            new_slave['progress'] = QProgressBar()
            new_slave['work'] = 0
            new_slave['label'] = QLabel('Worker ==> {}'.format(slave_id))
            self.slave_layout.addWidget(new_slave['label'])

            self.slave_layout.addWidget(new_slave['progress'])
            new_slave['progress'].setValue(0)

            self.slave_workers.append(new_slave)
        elif slave_id != 0:
            for slave in self.slave_workers:
                if slave['id'] == slave_id:
                    if msg == 'update':
                        slave['work'] += 1
                        slave['progress'].setValue(100 / self._server.WORK_SIZE * slave['work'])
                    elif msg == 'done':
                        slave['progress'].setValue(0)
                        slave['work'] = 0
                    elif msg == 'die':
                        slave['progress'].deleteLater()
                        slave['label'].deleteLater()
                    else:
                        print("Unknown message: " + msg) 
        else:
            for i in range(self.attributes_listbox.count()):
                if self.attributes_listbox.item(i).text() == msg:
                    self.attributes_listbox_out.addItem(self.attributes_listbox.takeItem(i))
                    break

    def update_listener(self, progress:int):
        self._progress_bar.setValue(math.floor(100 / self.total_progress * (progress + 1)))

        if progress + 1 == self.total_progress:
            self.reset_buttons()

    def reset_buttons(self):
        self._thread.is_active = False
        self._is_working = False
        self._stop_proc_button.setEnabled(False)

    def initUI(self):
        def _select_directory():
            in_selected_arff.clear()
            check = QFileDialog.getExistingDirectory(None, 'Select directory', str(sys.path[0]))
            if not check:
                return
            self.attributes_listbox.clear()
            self.attributes_listbox_out.clear()
            in_selected_arff.setText(check)
            for att in self._server.get_image_paths(check):
                item = QListWidgetItem("%s" % (str(att)))
                self.attributes_listbox.addItem(item)
            self.total_progress:int = self.attributes_listbox.count()
            self._flag_init = True

        def _start_process():
            if self._is_working:
                QMessageBox.critical(None, "Error", "Can't start a new task without finishing or stopping the previous one")
                return

            if not self._flag_init: 
                QMessageBox.critical(None, "Error", "No Starting Directory selected!")
                return

            self.update_listener(0)
            self.attributes_listbox_out.clear()
            self.attributes_listbox.clear()
            for att in self._server.get_image_paths(in_selected_arff.text()):
                item = QListWidgetItem("%s" % (str(att)))
                self.attributes_listbox.addItem(item)
            self.total_progress:int = self.attributes_listbox.count()

            self._is_working = True
            self._stop_proc_button.setEnabled(True)
            self._thread.start()
            
            try:
                self._server.start(in_selected_arff.text())
            except Exception as err:
                _stop_process()
                QMessageBox.critical(None, "Error", str(err))

        def _stop_process():
            self.reset_buttons()
            self._server.stop()

        self._progress_bar = QProgressBar()
        self._progress_bar.setValue(0)

        grid_box_lay = QGridLayout()
        button_layout = QHBoxLayout()

        in_select_button = QPushButton('Select')
        in_select_button.clicked.connect(_select_directory)
        button_layout.addWidget(in_select_button)

        in_selected_arff = QLineEdit()
        in_selected_arff.setReadOnly(True)
        in_selected_arff.setPlaceholderText("Press 'Select' to choose the start")
        button_layout.addWidget(in_selected_arff)

        lab1 = QLabel("To read:")
        grid_box_lay.addWidget(lab1, 1, 0, 1, 1)
        self.attributes_listbox = QListWidget()
        grid_box_lay.addWidget(self.attributes_listbox, 2, 0, 1, 1)

        lab1 = QLabel("Done:")
        grid_box_lay.addWidget(lab1, 1, 1, 1, 1)
        self.attributes_listbox_out = QListWidget()
        grid_box_lay.addWidget(self.attributes_listbox_out, 2, 1, 1, 1)

        start_proc_button = QPushButton('Start')
        start_proc_button.clicked.connect(_start_process)
        button_layout.addWidget(start_proc_button)

        self._stop_proc_button = QPushButton('Stop')
        self._stop_proc_button.setEnabled(False)
        self._stop_proc_button.clicked.connect(_stop_process)
        button_layout.addWidget(self._stop_proc_button)

        grid_box_lay.addWidget(self._progress_bar, 3, 0, 1, 2)

        main_vbox = QGridLayout()

        main_vbox.setColumnStretch(1, 3)
        main_vbox.setColumnStretch(0, 1)

        input_gbox = QGroupBox("Input")
        input_gbox.setLayout(button_layout)
        main_vbox.addWidget(input_gbox, 0, 1)

        attributes_group = QGroupBox("Results")
        attributes_group.setLayout(grid_box_lay)
        main_vbox.addWidget(attributes_group, 1, 1)

        self.slave_layout = QVBoxLayout()
        slave_parent = QVBoxLayout()
        slave_parent.addLayout(self.slave_layout)
        slave_parent.addStretch()
        slave_group = QGroupBox("Workers:")
        slave_group.setLayout(slave_parent)
        main_vbox.addWidget(slave_group, 0, 0, 2, 1)

        self.setLayout(main_vbox)
        self.setWindowTitle("PD5 Tesseract")
        self.setGeometry(300, 300, 1024, 640)
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = PyQtGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

