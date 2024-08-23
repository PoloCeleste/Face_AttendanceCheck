import facecheck, sys
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QStatusBar, QDialog, QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QLCDNumber, QFrame, QDesktopWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QTime, QDate

class MyApp(QMainWindow, QDialog, QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)
        
        self.time = QTime.currentTime()
        self.date = QDate.currentDate()
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.dialog=QDialog()
        self.timer.start()
        self.initUI()
        

    def initUI(self):
        lt = QVBoxLayout()
        pic=QPixmap("LogoLong.png")
        fnt=QFont("D2Coding", 30, QFont.Bold)

        imlbl = QLabel(self)
        imlbl.setGeometry(40, 40, 200, 67)
        imlbl.setPixmap(pic)
        imlbl.setScaledContents(True)

        lbl = QLabel("안면인식 출석체크 시스템", self)
        lbl.setFont(QFont("D2Coding", 50, QFont.Bold))
        lbl.setGeometry(530, 150, 820, 80)

        Ylbl = QLabel(self)
        Ylbl.setFont(fnt)
        Ylbl.setText(self.date.toString(Qt.DefaultLocaleShortDate))
        Ylbl.setGeometry(830, 320, 220, 60)

        self.lcd = QLCDNumber(self)
        self.lcd.display('')
        self.lcd.setFrameStyle(QFrame.NoFrame)
        self.lcd.setDigitCount(8)
        self.lcd.setGeometry(730, 390, 400, 120)
        self.lcd.setSegmentStyle(2)

        self.loglbl =  QLabel('', self)
        self.loglbl.setFont(QFont("D2Coding", 40, QFont.Bold))
        self.loglbl.setGeometry(530, 920, 820, 160)
        
        self.sbtn = QPushButton('Start', self)
        self.sbtn.setGeometry(870, 600, 140, 55)
        self.sbtn.setFont(fnt)
        self.sbtn.setDefault(True)
        self.sbtn.clicked.connect(facecheck.faceRecog)
        
        self.sbtn = QPushButton('Regist', self)
        self.sbtn.setGeometry(870, 700, 140, 55)
        self.sbtn.setFont(fnt)
        self.sbtn.clicked.connect(self.faceRegist)
        
        qbtn = QPushButton('Quit', self)
        qbtn.setGeometry(870, 800, 140, 55)
        qbtn.setFont(fnt)
        qbtn.clicked.connect(self.closeMessage)

        lt.addWidget(lbl)
        lt.addWidget(self.lcd)
        lt.addWidget(self.loglbl)
        lt.addWidget(self.sbtn)
        lt.addWidget(qbtn)

        self.setLayout(lt)
        self.setWindowTitle('안면인식 출석체크 시스템')
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.statusBar.showMessage(self.date.toString(Qt.DefaultLocaleLongDate))
        self.resize(1920, 1080)
        self.center()
        self.showFullScreen()

    def timeout(self):
        sender = self.sender()
        currentTime = QTime.currentTime().toString("hh:mm:ss")
        if id(sender) == id(self.timer):
            self.lcd.display(currentTime)
    
    def faceRegist(self):
        facecheck.makeDataset()
        facecheck.trainingData()
        f = open("Regist.txt", 'a')
        text, ok = QInputDialog.getText(self, 'Registration', 'Enter your name:')
        if ok:
            f.write('\n'+str(text))
        f.close()
        self.loglbl.setText('Resistration : '+text)
        
    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeMessage(self):
        message = QMessageBox.question(self, "Question", "Are you sure you want to quit?")
        if message == QMessageBox.Yes:
            sys.exit()
            
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())