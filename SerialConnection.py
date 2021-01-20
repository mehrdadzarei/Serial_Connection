
# serial connection
# author: Mehrdad Zarei
# e-mail: mehr.zarei1@gmail.com
# date: 18.11.2020

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, time
import serial
import serial.tools.list_ports as lp

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Terminal')
        # self.resize(500,400)
        self.setGeometry(400, 200, 500, 400)
        # self.showMaximized()
        QApplication.setStyle('Fusion')
        # background-color: black; color: white; 
        self.setStyleSheet('font-size: 11pt;')
        icon = QIcon()
        icon.addPixmap(QPixmap("icons\Terminal.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.centralWidget=QWidget()
        mainLayout = QGridLayout()

        self.receiveText = ''
        baudRates = ['110', '300', '600', '1200', '2400', '4800', '9600',
                     '14400', '19200', '38400', '57600', '115200', '128000', '256000']
        comPorts = list(lp.comports())
        comID = []
        self.lenI = len(comPorts)
        for i in range(self.lenI):
            comID.append(comPorts[i][0])
        self.serialOk = 0
        self.portD = ''
        self.readLen = 100
        self.writeLen = 100

        # setting 
        self.port = QComboBox()
        self.port.addItems(comID)

        portLabel = QLabel("&Port:")
        portLabel.setBuddy(self.port)
        
        self.baudRate = QComboBox()
        self.baudRate.addItems(baudRates)
        self.baudRate.setCurrentIndex(11)

        baudRateLabel = QLabel("&Baud Rate:")
        baudRateLabel.setBuddy(self.baudRate)

        self.connectH = QPushButton('Connect')
        self.connectH.setDefault(True)
        self.connectH.setEnabled(True)
                
        # data
        self.transmit = QLineEdit('')
        
        transmitLabel = QLabel("&Transmit:")
        transmitLabel.setBuddy(self.transmit)
        
        self.send = QPushButton('Send')
        self.send.setDefault(True)
        self.send.setEnabled(False)

        self.receive = QTextEdit()
        self.receive.setReadOnly(True)
        self.receive.setStyleSheet('background-color: black; color: white;')
        # self.receive.setPlainText(self.receiveText)
        self.receive.moveCursor(QTextCursor.End)

        receiveLabel = QLabel("&Receive:")
        receiveLabel.setBuddy(self.receive)

        # function connection 
        # self.port.activated[str].connect(self.setPort)
        # self.baudRate.activated[str].connect(self.setBaudRate)
        self.send.clicked.connect(self.sendData)
        self.connectH.clicked.connect(self.connectDevice)
        
        mainLayout.addWidget(portLabel, 0, 0)
        mainLayout.addWidget(self.port, 1, 0)
        mainLayout.addWidget(baudRateLabel, 0, 1)
        mainLayout.addWidget(self.baudRate, 1, 1)
        mainLayout.addWidget(self.connectH, 1, 2)

        mainLayout.addWidget(transmitLabel, 2, 0)
        mainLayout.addWidget(self.transmit, 3, 0, 1, 2)
        mainLayout.addWidget(self.send, 3, 2)
        mainLayout.addWidget(receiveLabel, 4, 0)
        mainLayout.addWidget(self.receive, 5, 0, 3, 3)
        # mainLayout.setRowStretch(1, 1)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setRowStretch(3, 1)
        # mainLayout.setRowStretch(4, 1)
        mainLayout.setRowStretch(5, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.centralWidget.setLayout(mainLayout)
        self.setCentralWidget(self.centralWidget)

    # def setPort(self):

        # self.portH = self.port.currentText()
        # self.receiveText += '\n' + self.portH
        # self.receive.setPlainText(self.receiveText)

    # def setBaudRate(self):

        # self.baudRateH = self.baudRate.currentText()
        # self.receiveText += '\n' + self.baudRateH
        # self.receive.setPlainText(self.receiveText)

    def sendData(self):

        self.serialOk = 0
        message = str(self.transmit.text())
        msg_length = str(len(message))
        send_length = msg_length + ' ' * (self.writeLen - len(msg_length))

        if self.ser.is_open:

            self.ser.write(send_length.encode())
            self.ser.write(message.encode())
        else:

            self.ser.open()
            self.ser.write(send_length.encode())
            self.ser.write(message.encode())
        self.serialOk = 1

    def receiveData(self):

        try:

            text = self.ser.read(self.readLen).decode("utf-8").strip()
            if text:
                self.receiveText += text + "\n"
                self.receive.setPlainText(self.receiveText)
                self.receive.moveCursor(QTextCursor.End)
        except: pass
        
    def connectDevice(self):

        comD = self.port.currentText()
        baudRateD = int(self.baudRate.currentText())

        try:

            self.ser = serial.Serial(comD, baudRateD, timeout = 0.1)
            self.ser.close()
            self.serialOk = 1
            self.portD = comD
            self.send.setEnabled(True)
            self.connectH.setEnabled(False)
            self.receiveText = 'connected\n' 
            self.receive.setPlainText(self.receiveText)
            self.receive.moveCursor(QTextCursor.End)
        except:

            self.serialOk = 0
            self.send.setEnabled(False)
            self.connectH.setEnabled(True)
            self.receiveText = 'not connected\n' 
            self.receive.setPlainText(self.receiveText)
            self.receive.moveCursor(QTextCursor.End)
            pass

    def update(self):
        
        comPorts = list(lp.comports())
        comID = []
        self.lenC = len(comPorts)
        if self.lenC != self.lenI:

            self.lenI = self.lenC
            for i in range(self.lenC):
                comID.append(comPorts[i][0])
            self.port.clear()
            self.port.addItems(comID)

            if self.portD not in comID:

                self.serialOk = 0
                self.send.setEnabled(False)
                self.connectH.setEnabled(True)
                self.receiveText += '\nnot connected' 
                self.receive.setPlainText(self.receiveText)
                self.receive.moveCursor(QTextCursor.End)

                

        if self.serialOk:

            if self.ser.is_open:

                self.receiveData()
            else:

                self.ser.open()
                self.receiveData()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    timer = QTimer()
    timer.setInterval(100)
    timer.timeout.connect(ui.update)
    timer.start()
    sys.exit(app.exec_())

