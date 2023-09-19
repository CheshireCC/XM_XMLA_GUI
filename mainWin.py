'''
Descripttion: 主窗体
version: 0.1
Author: Cheshire
Date: 2023-09-18 17:29:17
LastEditors: Cheshire
LastEditTime: 2023-09-19 03:18:08
'''

import sys
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import QObject, Signal

from Ximalaya_XM_Decrypt import decrypt_xm_file

import os

from UI_mainWindows import mainWin_UI

class RedirectOutputSignalStore(QObject):
    outputSignal = Signal(str)
    def fileno(self):
        return -1
    def write(self, text):
        if(not self.signalsBlocked()):
            self.outputSignal.emit(str(text))

class mainWin(mainWin_UI):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.signalAndSlot()
        self.redirectOutput(self.setTextAndMoveCursorToTextBrowser)

        self.LineEdit_input.setClearButtonEnabled(True)
        self.LineEdit_output.setClearButtonEnabled(True)


    def setTextAndMoveCursorToTextBrowser(self, text:str):
        self.textBrowser.moveCursor(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
        self.textBrowser.insertPlainText(text)

    def redirectOutput(self, target:callable):
        # 重定向输出
        sys.stdout = RedirectOutputSignalStore()
        sys.stdout.outputSignal.connect(target)
        sys.stderr = RedirectOutputSignalStore()
        sys.stderr.outputSignal.connect(target)

    def on_PushButon_input_clicked(self):
        filenames,_ = QFileDialog.getOpenFileNames(self, "选择文件", r"./", "喜马拉雅 xm(*.xm)")
        # print(filenames)

        if len(filenames)>0:
            filenames_text = ";".join(filenames)
        self.LineEdit_input.setText(filenames_text)
    
    def on_PushButon_output_clicked(self):
        dir_out = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if dir_out:
            self.LineEdit_output.setText(dir_out)
    
    def on_PushButon_process_clicked(self):
        fileList = self.LineEdit_input.text().split(";")
        # print(fileList)
        output_path = self.LineEdit_output.text()

        for file in fileList:
            print(f"[current task: {file}]")
            if not(os.path.exists(file)):
                print(f"无效文件，跳过：{file}")
                continue
            
            if output_path == "":
                output_path,_ = os.path.split(file)
                # print(output_path)
            
            decrypt_xm_file(from_file=file,output_path=output_path)
            

    def signalAndSlot(self):
        self.PushButon_input.clicked.connect(self.on_PushButon_input_clicked)
        self.PushButon_output.clicked.connect(self.on_PushButon_output_clicked)
        self.PushButton_process.clicked.connect(self.on_PushButon_process_clicked)
        