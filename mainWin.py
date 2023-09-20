'''
Descripttion: 主窗体
version: 0.1
Author: Cheshire
Date: 2023-09-18 17:29:17
LastEditors: Cheshire
LastEditTime: 2023-09-20 21:52:33
'''

import sys
# from concurrent import futures

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Signal

from Ximalaya_XM_Decrypt import decrypt_xm_file
from threading import Thread

import os

from UI_mainWindows import mainWin_UI

class RedirectOutputSignalStore(QObject):
    outputSignal = Signal(str)
    def fileno(self):
        return -1
    def write(self, text):
        if(not self.signalsBlocked()):
            self.outputSignal.emit(str(text))
    def flush(self):
        pass


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

    def excutor_decrypt_xm_file(self, **kargs):
        file = kargs["file"]
        output_path = kargs['output_path']
        print(file, output_path)
        decrypt_xm_file(from_file=file, output_path=output_path)
        return "\n"


    def on_PushButon_process_clicked(self):
        self.textBrowser.clear()

        fileList = self.LineEdit_input.text().split(";")
        # print(fileList)
        output_path = self.LineEdit_output.text()

        if output_path != "":
            if not os.path.exists(output_path):
                try:
                    os.mkdir(output_path)
                except:
                    output_path = ""
        
        # with futures.ThreadPoolExecutor(4) as excutor:

        #     file_out_List = []
        #     for i in range(len(fileList)):
        #         fileList.append({"file":fileList[i], "output_path":output_path})

        #     results = excutor.map(self.excutor_decrypt_xm_file, file_out_List)
            
        #     for r in results:
        #         print(type(r))
        
        def run(fileList:list, output_path:str):
            for file in fileList:
                
                print(f"[current task: {file}]")
                if not(os.path.exists(file)) or not(os.path.isfile(file)):
                    print(f"无效文件，跳过：{file}")
                    continue
                
                if output_path == "":
                    output_path,_ = os.path.split(file)
                    # print(output_path)
                
                decrypt_xm_file(from_file=file, output_path=output_path)
                print("\n")
            
            print("[over!]")

        thread_dxf = Thread(target=run, daemon=True, args=(fileList, output_path))
        thread_dxf.start()


    def signalAndSlot(self):
        self.PushButon_input.clicked.connect(self.on_PushButon_input_clicked)
        self.PushButon_output.clicked.connect(self.on_PushButon_output_clicked)
        self.PushButton_process.clicked.connect(self.on_PushButon_process_clicked)
        