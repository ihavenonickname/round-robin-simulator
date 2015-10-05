import sys
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import Qt

from controller import ProcessesHandler

class SetupWindow(QWidget):
    def __init__(self):
        super(SetupWindow, self).__init__()

        self.setWindowTitle("Round-robin simulator")

        left = QVBoxLayout()
        left.addWidget(QLabel("Quantum"))
        left.addWidget(QLabel("Maximum life time"))
        left.addWidget(QLabel("Processes per minute"))
        left.addWidget(QLabel("Chance to be I/O Bound"))
        left.addWidget(QLabel("Duration of each cicle"))

        right = QVBoxLayout()
        self.lineEdits = []

        for i in range(5):
            self.lineEdits.append(QLineEdit())
            right.addWidget(self.lineEdits[i])

        top = QHBoxLayout()
        top.addLayout(left)
        top.addLayout(right)

        bottom = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startSimulator)
        bottom.addStretch(1)
        bottom.addWidget(self.startButton)
        bottom.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addLayout(bottom)
        self.setLayout(layout)

        self.setFixedSize(self.sizeHint())

        self.simulatorIsOpened = False

    def getInput(self):
        return [int(l.text()) for l in self.lineEdits]

    def startSimulator(self):
        if self.simulatorIsOpened:
            return

        try:
            values = self.getInput()
        except:
            QMessageBox.critical(self, "Erro", 'Valores estranhos')
            return

        self.w = SimulatorWindow(self, values)
        self.w.showMaximized()
        self.simulatorIsOpened = True

class SimulatorWindow(QWidget):
    def __init__(self, setupWindow, values):
        super(SimulatorWindow, self).__init__()
        self.setWindowTitle("Round-Robin simulator")

        self.setupWindow = setupWindow

        left = QVBoxLayout()
        self.waitingProcessesList = QListWidget()
        left.addWidget(QLabel('Waiting'))
        left.addWidget(self.waitingProcessesList)

        right = QVBoxLayout()
        self.readyProcessesList = QListWidget()
        right.addWidget(QLabel('Ready'))
        right.addWidget(self.readyProcessesList)

        top = QHBoxLayout()
        top.addLayout(left)
        top.addLayout(right)

        bottom = QVBoxLayout()
        self.labels = []
        self.labels.append(QLabel('current process'))
        self.labels.append(QLabel('runs'))
        self.labels.append(QLabel('time to create'))
        self.labels.append(QLabel('finished'))
        for label in self.labels:
            label.setFont(QFont('Lucida Console', 20))
            bottom.addWidget(label)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addLayout(bottom)
        self.setLayout(layout)

        self.processesHandler = ProcessesHandler(parent=self,
                                                quantum=values[0],
                                                maxLifeTime=values[1],
                                                maxPerMinute=values[2],
                                                chanceToBeIoBound=values[3],
                                                cicleDuration=values[4]/1000.0)

        self.processesHandler.runCompleted.connect(self.updateInfos)
        self.processesHandler.start()

    def closeEvent(self, event):
        self.processesHandler.stop()
        self.setupWindow.simulatorIsOpened = False

    def updateInfos(self):
        self.readyProcessesList.clear()
        for p in self.processesHandler.ready:
            self.readyProcessesList.addItem(str(p))

        self.waitingProcessesList.clear()
        for p in self.processesHandler.waiting:
            self.waitingProcessesList.addItem(str(p))

        processName = str(self.processesHandler.currentProcess)
        self.labels[0].setText('Current process: ' + processName)

        number = str(self.processesHandler.howManyRunsInCurrentProcess)
        self.labels[1].setText('Runs in current process: ' + number)

        seconds = str(self.processesHandler.secondsSinceLastCreation)
        self.labels[2].setText('Seconds since last creation: ' + seconds)

        finished = str(self.processesHandler.processesFinished)
        self.labels[3].setText('Total processes finished: ' + finished)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SetupWindow()
    w.show()
    sys.exit(app.exec_())
