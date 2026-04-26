import sys
import os
import sysv_ipc
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from databaseManager import DatabaseManager
from communicationManager import CommunicationManager

class Login(QtWidgets.QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(ROOT_DIR, 'login.ui')

    def __init__(self):
        super().__init__()
        uic.loadUi(self.ui_path, self)
        self.setWindowTitle('X&0 Login')
        self.login.clicked.connect(self.handleLogin)

    def handleLogin(self):
        if self.playerName.text().strip() == '':
            QtWidgets.QMessageBox.warning(self, "Eroare", "Introdu numele tău!")
            return
        self.accept()

    def getUserData(self):
        return self.playerName.text().strip()

class MainWindow(QtWidgets.QMainWindow):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(ROOT_DIR, 'game.ui')

    def __init__(self, myName, role, oponentName, db):
        super().__init__()
        uic.loadUi(self.ui_path, self)
        self.setWindowTitle('X&0')

        self.myName = myName
        self.role = role
        self.oponentName = oponentName
        self.p1Db = self.myName if self.role==1 else self.oponentName
        self.p2Db = self.oponentName if self.role==1 else self.myName
        self.db = db
        self.isMyTurn = (role == 1)
        self.mySymbol = "X" if self.role==1 else "0"
        self.oponentSymbol = "0" if self.role==1 else "X"
        self.btns = []

        id, p1Score, p2Score, player1, player2, lastPlayed = self.db.getScore(player1=self.myName, player2=self.oponentName)
        if id==None:
            self.db.saveScore(player1=self.p1Db, player2=self.p2Db, score=0)
            id, p1Score, p2Score, player1, player2, lastPlayed = self.db.getScore(player1=self.myName, player2=self.oponentName)
            self.p1Score = p1Score
            self.p2Score = p2Score
            self.lastPlayed = lastPlayed
        else:
            if player1 == self.myName:
                self.p1Score = p1Score
                self.p2Score = p2Score
            else:
                self.p1Score = p2Score
                self.p2Score = p1Score
            self.lastPlayed = lastPlayed

        self.p1.setText(f"Eu: {self.myName}")
        self.p2.setText(f"Adversar: {self.oponentName}")
        self.status.setText("Randul tau!" if self.isMyTurn else "Randul adversarului!")
        self.score.setText(f"Scor: {self.myName}: {self.p1Score} - {self.oponentName}: {self.p2Score}")
        self.lastGame.setText(f"Ultimul joc: {self.lastPlayed}")

        self.comm = CommunicationManager(role=role)
        self.comm.move_received.connect(self.handleReceived)
        self.comm.start()

        for i in range(9):
            btn = self.findChild(QtWidgets.QPushButton, 'btn' + str(i))
            self.btns.append(btn)
            self.btns[i].clicked.connect(lambda _, idx = i: self.handle_click(idx))

    def handle_click(self, index):
        if self.isMyTurn and self.btns[index].text()=="":
            self.btns[index].setText(self.mySymbol)
            self.btns[index].setStyleSheet("font-size: 30px; color: blue; font-weight: bold;")
            self.btns[index].setEnabled(False)

            self.isMyTurn = False
            self.status.setText("Randul adversarului!")


            status = self.checkWin()
            if status != -1:
                self.db.saveScore(player1=self.p1Db, player2=self.p2Db, score=status)
                self.comm.sendMove(index=index)
                self.reset()
                if status == self.role:
                    QMessageBox.information(self, "Game over!", "You win!")
                elif status > 0 and status!=self.role:
                    QMessageBox.information(self, "Game over!", "You lose!")
                elif status == 0:
                    QMessageBox.information(self, "Game over!", "Equal!")
            else:
                self.comm.sendMove(index=index)

    def handleReceived(self, index):
        if self.btns[index].text() == "":
            self.btns[index].setText(self.oponentSymbol)
            self.btns[index].setStyleSheet("font-size: 30px; color: red; font-weight: bold;")
            self.btns[index].setEnabled(False)

            self.isMyTurn = True
            self.status.setText("Randul tau!")
            status = self.checkWin()
            if status != -1:
                self.reset()
                if status == self.role:
                    QMessageBox.information(self, "Game over!", "You win!")
                elif status > 0 and status != self.role:
                    QMessageBox.information(self, "Game over!", "You lose!")
                elif status == 0:
                    QMessageBox.information(self, "Game over!", "Equal!")

    def checkWin(self):
        line1 = self.btns[0].text() + self.btns[1].text() + self.btns[2].text()
        line2 = self.btns[3].text() + self.btns[4].text() + self.btns[5].text()
        line3 = self.btns[6].text() + self.btns[7].text() + self.btns[8].text()
        col1 = self.btns[0].text() + self.btns[3].text() + self.btns[6].text()
        col2 = self.btns[1].text() + self.btns[4].text() + self.btns[7].text()
        col3 = self.btns[2].text() + self.btns[5].text() + self.btns[8].text()
        diag1 = self.btns[0].text() + self.btns[4].text() + self.btns[8].text()
        diag2 = self.btns[2].text() + self.btns[4].text() + self.btns[6].text()

        combo1 = "X" * 3
        combo2 = "0" * 3

        if line1 == combo1 or line2 == combo1 or line3 == combo1 or col1 == combo1 or col2 == combo1 or col3 == combo1 or diag1 == combo1 or diag2 == combo1:
            return 1
        elif line1 == combo2 or line2 == combo2 or line3 == combo2 or col1 == combo2 or col2 == combo2 or col3 == combo2 or diag1 == combo2 or diag2 == combo2:
            return 2
        elif all(btn.text() != "" for btn in self.btns):
            return 0
        else:
            return -1

    def reset(self):
        id, p1Score, p2Score, player1, player2, lastPlayed = self.db.getScore(player1=self.myName, player2=self.oponentName)
        if id == None:
            self.db.saveScore(player1=self.p1Db, player2=self.p2Db, score=0)
            id, p1Score, p2Score, player1, player2, lastPlayed = self.db.getScore(player1=self.myName, player2=self.oponentName)
            self.p1Score = p1Score
            self.p2Score = p2Score
            self.lastPlayed
        else:
            if player1 == self.myName:
                self.p1Score = p1Score
                self.p2Score = p2Score
            else:
                self.p1Score = p2Score
                self.p2Score = p1Score
            self.lastPlayed = lastPlayed

        self.p1.setText(f"Eu: {self.myName}")
        self.p2.setText(f"Adversar: {self.oponentName}")
        self.status.setText("Randul tau!" if self.isMyTurn else "Randul adversarului!")
        self.score.setText(f"Scor: {self.myName}: {self.p1Score} - {self.oponentName}: {self.p2Score}")
        self.lastGame.setText(f"Ultimul joc: {self.lastPlayed}")
        for btn in self.btns:
            btn.setEnabled(True)
            btn.setText("")
            btn.setStyleSheet("")

def getRoles(myName):
    try:
        messageQueue = sysv_ipc.MessageQueue(1234, sysv_ipc.IPC_CREAT)
        try:
            msg, mtype = messageQueue.receive(block=False, type=11)
            p1Name = msg.decode()
            messageQueue.send(myName.encode(), type=21)
            return 2, p1Name
        except sysv_ipc.BusyError:
            clearQueue(1234)
            messageQueue.send(myName.encode(), type=11)
            print("Astept adversar")
            msg, mtype = messageQueue.receive(block=True, type=21)
            p2Name = msg.decode()
            return 1, p2Name
    except:
        print("Eroare la conectare")
        return None, None

def clearQueue(key = 1234):
    try:
        print("Curatare coada")
        messageQueue = sysv_ipc.MessageQueue(key)
        while True:
            messageQueue.receive(block=False, type=0)
    except sysv_ipc.BusyError:
        print("Coada e goala")
    except sysv_ipc.ExistentialError:
        print("Coada nu exista")
    except Exception as e:
        print(f"Eroare la curățarea cozii: {e}")


if __name__ == '__main__':
    db = DatabaseManager()
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    if login.exec_() == QtWidgets.QDialog.Accepted:
        userName = login.getUserData()
        role, oponentName = getRoles(userName)
        if role and userName != oponentName:
            window = MainWindow(userName, role, oponentName, db)
            window.show()
            sys.exit(app.exec_())
    sys.exit(0)