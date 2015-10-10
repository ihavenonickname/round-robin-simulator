from PyQt4.QtGui import *
from PyQt4.Qt import *

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
        self.waitingLabel = QLabel('Waiting: 0')
        left.addWidget(self.waitingLabel)
        left.addWidget(self.waitingProcessesList)

        middle = QVBoxLayout()
        self.readyProcessesList = QListWidget()
        self.readyLabel = QLabel('Ready')
        middle.addWidget(self.readyLabel)
        middle.addWidget(self.readyProcessesList)

        right = QVBoxLayout()
        self.labels = []
        self.labels.append(QLabel('life time'))
        self.labels.append(QLabel('runs'))
        self.labels.append(QLabel('time to create'))
        self.labels.append(QLabel('finished'))

        right.addStretch(1)

        for label in self.labels:
            label.setFont(QFont('Lucida Console', 16))
            right.addWidget(label)

        right.addStretch(1)


        layout = QHBoxLayout()
        layout.addLayout(left)
        layout.addLayout(middle)
        layout.addLayout(right)
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
        self.updateLabels()
        self.updateLists()

    def updateLists(self):
        self.readyProcessesList.clear()
        items = [str(p) for p in self.processesHandler.ready]
        self.readyProcessesList.addItems(items)

        self.waitingProcessesList.clear()
        items = [str(p) for p in self.processesHandler.waiting]
        self.waitingProcessesList.addItems(items)

    def updateLabels(self):
        processesReady = len(self.processesHandler.ready)
        self.readyLabel.setText("Ready: %d" % processesReady)

        processesWaiting = len(self.processesHandler.waiting)
        self.waitingLabel.setText("Waiting: %d" % processesWaiting)

        try:
            lifeTime = str(self.processesHandler.currentProcess.lifeTime)
        except:
            lifeTime = ""
        self.labels[0].setText("Current process' life time: " + lifeTime)

        qnt = str(self.processesHandler.ciclesInCurrentProcess)
        self.labels[1].setText('Cicles in current process: ' + qnt)

        seconds = self.processesHandler.secondsSinceLastCreation
        self.labels[2].setText("Seconds since last creation:%7.2f" % seconds)

        finished = str(self.processesHandler.processesFinished)
        self.labels[3].setText('Processes finished: ' + finished)
