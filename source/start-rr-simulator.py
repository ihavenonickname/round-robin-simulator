import sys

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication

from view import SetupWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SetupWindow()
    w.show()
    sys.exit(app.exec_())
