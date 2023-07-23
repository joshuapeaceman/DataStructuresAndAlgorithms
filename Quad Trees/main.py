import json
import sys
import traceback

import AppController
from PyQt6.QtWidgets import QApplication


sys.setrecursionlimit(3000)
print(sys.getrecursionlimit())


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        appCtrl = AppController.AppController()

        sys.exit(app.exec())
    except:
        traceback.print_exc()

