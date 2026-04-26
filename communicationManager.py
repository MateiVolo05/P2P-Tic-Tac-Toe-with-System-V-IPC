import sysv_ipc
from PyQt5.QtCore import QThread, pyqtSignal

class CommunicationManager(QThread):
    move_received = pyqtSignal(int)
    name_received = pyqtSignal(str)

    def __init__(self, role):
        super().__init__()
        self.role = role
        if role==1:
            self.myMoveType = 10
            self.opponentMoveType = 20
        else:
            self.myMoveType = 20
            self.opponentMoveType = 10
        self.messageQueue = sysv_ipc.MessageQueue(1234, sysv_ipc.IPC_CREAT)

    def sendMove(self, index):
        msg = str(index)
        self.messageQueue.send(msg.encode(), type=self.myMoveType)

    def sendName(self, name):
        self.messageQueue.send(name.encode(), type=self.myNameType)

    def run(self):
        while True:
            try:
                msg, mType = self.messageQueue.receive(type=self.opponentMoveType)
                content = msg.decode()
                self.move_received.emit(int(content))
            except:
                continue