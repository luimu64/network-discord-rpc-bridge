from cgi import print_environ_usage
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from logic import connection_manager
import threading
import configparser


class SettingsWindow(QMainWindow):
    def open(self):
        settings.show()

    def saveConfig(self):
        config = configparser.ConfigParser()
        config['OPTIONS'] = {
            'HostIpAddress': self.ipTextField.text(),
            'HostPort': self.portTextField.text(),
            'VerboseOutput': self.verboseTextField.text()
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def __init__(self, connection, icon):
        super(SettingsWindow, self).__init__()
        self.setWindowTitle("Settings")
        self.setMinimumWidth(300)
        self.setWindowIcon(icon)
        layout = QVBoxLayout()

        ipLabel = QLabel('Host ip address')
        portLabel = QLabel('Host port number')
        verboseLabel = QLabel('Verbose logging')

        self.ipTextField = QLineEdit(connection.HOST)
        self.portTextField = QLineEdit(connection.PORT)
        self.verboseTextField = QLineEdit(str(connection.VERBOSE))

        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.saveConfig)

        layout.addWidget(ipLabel)
        layout.addWidget(self.ipTextField)
        layout.addWidget(portLabel)
        layout.addWidget(self.portTextField)
        layout.addWidget(verboseLabel)
        layout.addWidget(self.verboseTextField)
        layout.addWidget(saveButton)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


connection = connection_manager()
app = QApplication([])
menu = QMenu()
icon = QIcon("icon.png")
tray = QSystemTrayIcon()
settings = SettingsWindow(connection, icon)

app.setQuitOnLastWindowClosed(False)
tray.setIcon(icon)
tray.setVisible(True)

settingsItem = QAction("Settings")
settingsItem.triggered.connect(settings.open)
menu.addAction(settingsItem)

# Add a Quit option to the menu.
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

tray.setContextMenu(menu)


t = threading.Thread(target=connection.main, daemon=True)
t.start()
app.exec()
