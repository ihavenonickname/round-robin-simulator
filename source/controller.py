import random
import time

from PyQt4.QtCore import QThread, pyqtSignal

class Process:
    REQUESTED_IO, GOT_FINISHED, RAN_NORMALLY = range(3)

    def __init__(self, name, lifeTime, chanceToRequestIO=0):
        self.name = name
        self.lifeTime = lifeTime
        self.chanceToRequestIO = chanceToRequestIO
        self.ciclesToBeReady = 0

    def run(self):
        self.lifeTime -= 1

        if self.lifeTime == 0:
            return self.GOT_FINISHED

        if random.randint(1, 100) < self.chanceToRequestIO:
            self.ciclesToBeReady = random.randint(1, self.lifeTime * 3)
            return self.REQUESTED_IO

        return self.RAN_NORMALLY

    def returnedFromIo(self):
        self.ciclesToBeReady -= 1
        return self.ciclesToBeReady < 1

    def __str__(self):
        return self.name

class ProcessesHandler(QThread):
    runCompleted = pyqtSignal()

    def __init__(self, parent, quantum, maxLifeTime, maxPerMinute,
                                                     chanceToBeIoBound,
                                                     cicleDuration):

        QThread.__init__(self)

        self.parent = parent
        self.quantum = quantum
        self.maxLifeTime = maxLifeTime
        self.maxPerMinute = maxPerMinute
        self.chanceToBeIoBound = chanceToBeIoBound
        self.cicleDuration = cicleDuration

        self.currentProcess = None
        self.ready = []
        self.waiting = []
        self.howManyRunsInCurrentProcess = 0
        self.currentName = 0
        self.running = True
        self.secondsSinceLastCreation = 99999
        self.processesFinished = 0

    def stop(self):
        self.running = False

    def run(self):
        print 'run started'

        while self.running:
            if self.secondsSinceLastCreation >= 60:
                self.createProcesses()
                self.secondsSinceLastCreation = 0

            self.runCurrentProcess()
            self.checkWaitingProcesses()

            time.sleep(self.cicleDuration)
            self.secondsSinceLastCreation += self.cicleDuration

            self.runCompleted.emit()

        print 'run stopped'

    def createProcesses(self):
        howManyNewProcesses = random.randint(self.maxPerMinute / 2,
                                             self.maxPerMinute+1)

        for i in range(howManyNewProcesses):
            lifeTime = random.randint(1, self.maxLifeTime+1)
            name = self.nextName()
            if random.randint(1, 100) < self.chanceToBeIoBound:
                chanceToRequestIO = random.randint(1, 100)
                self.ready.insert(0, Process(name, lifeTime, chanceToRequestIO))
            else:
                self.ready.insert(0, Process(name, lifeTime))

    def runCurrentProcess(self):
        if self.currentProcess is None:
            if not self.goNextProcess():
                return

        status = self.currentProcess.run()
        self.howManyRunsInCurrentProcess += 1

        if status == Process.GOT_FINISHED:
            self.goNextProcess()
            self.howManyRunsInCurrentProcess = 0
            self.processesFinished += 1
        elif status == Process.REQUESTED_IO:
            self.waiting.append(self.currentProcess)
            self.goNextProcess()
            self.howManyRunsInCurrentProcess = 0
        elif self.howManyRunsInCurrentProcess >= self.quantum:
            self.ready.insert(0, self.currentProcess)
            self.goNextProcess()
            self.howManyRunsInCurrentProcess = 0

    def goNextProcess(self):
        if self.ready:
            self.currentProcess = self.ready.pop()
            return True

        self.currentProcess = None
        return False

    def checkWaitingProcesses(self):
        for process in self.waiting:
            if process.returnedFromIo():
                self.ready.insert(0, process)
                self.waiting.remove(process)

    def nextName(self):
        if self.currentName == 10**10:
            self.currentName = 0

        self.currentName += 1

        return "%010d" % self.currentName

    def hasSomethingToDo(self):
        return (self.ready or
                self.waiting or
                self.currentProcess is not None)
