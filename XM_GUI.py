'''
Descripttion: 主程序入口
version: 0.1
Author: Cheshire
Date: 2023-09-18 17:28:48
LastEditors: Cheshire
LastEditTime: 2023-09-19 03:17:26
'''
import sys

from mainWin import mainWin
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    mainWindows = mainWin()
    mainWindows.show()
    sys.exit(app.exec())
    
