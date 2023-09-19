'''
Descripttion: UI设计文件
version: 0.1
Author: Cheshire
Date: 2023-09-18 17:28:21
LastEditors: Cheshire
LastEditTime: 2023-09-19 03:18:34
'''

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qframelesswindow import FramelessMainWindow, StandardTitleBar

from qfluentwidgets import LineEdit, PushButton, ToolButton, setTheme, Theme
from PySide6.QtWidgets import QLabel, QSpacerItem, QStyle, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QTextBrowser

from resource import rc_Image

class mainWin_UI(FramelessMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置主控件为窗体容器
        self.mainWidgets = QWidget(self)
        
        # 创建主布局
        self.mainLayout = QGridLayout()
        self.mainWidgets.setLayout(self.mainLayout)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setContentsMargins(30,30,30,30)
        # 设置中心控件为主控件
        self.setCentralWidget(self.mainWidgets)

        # 向主布局添加自定义布局
        self.VBoxLayout_main = QVBoxLayout()
        self.mainLayout.addLayout(self.VBoxLayout_main, 0, 0)

        # 添加空部件
        self.spaceItemTop = QSpacerItem(0,30)
        self.VBoxLayout_main.addItem(self.spaceItemTop)
        
        # 设置布局内控件向上对齐
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        
        # 窗体基本设置 
        self.initUI()
        # 添加控件、完成窗体
        self.setupUI()

        # 设置层到最后 避免遮挡
        self.mainWidgets.lower()
        # self.lower()
        
    def setupUI(self):

        widgetsQGridLayout = QGridLayout()
        self.VBoxLayout_main.addLayout(widgetsQGridLayout)

        label_inputFiles = QLabel("输入文件、可多选")
        self.LineEdit_input = LineEdit()
        self.LineEdit_input.setPlaceholderText("文件完整路径，多文件用 ; 分割")
        self.PushButon_input = ToolButton()
        self.PushButon_input.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_FileIcon))

        widgetsQGridLayout.addWidget(label_inputFiles,0,0)
        widgetsQGridLayout.addWidget(self.LineEdit_input,0,1)
        widgetsQGridLayout.addWidget(self.PushButon_input,0,2)

        # 第二行
        label_outputFiles = QLabel("输出目录")
        self.LineEdit_output = LineEdit()
        self.LineEdit_output.setPlaceholderText("输出目录，不设置时默认为输入文件当前目录")
        self.PushButon_output = ToolButton()
        self.PushButon_output.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_DirIcon))

        widgetsQGridLayout.addWidget(label_outputFiles,1,0)
        widgetsQGridLayout.addWidget(self.LineEdit_output,1,1)
        widgetsQGridLayout.addWidget(self.PushButon_output,1,2)

        # 第三行
        spaceItem_01 = QSpacerItem(10,10)
        spaceItem_02 = QSpacerItem(10,10)
        self.PushButton_process = PushButton()
        self.PushButton_process.setText("处理")
        widgetsQGridLayout.addItem(spaceItem_01,2,0)
        widgetsQGridLayout.addItem(spaceItem_02,2,2)
        widgetsQGridLayout.addWidget(self.PushButton_process,2,1)

        # 文本输出
        self.textBrowser = QTextBrowser()
        self.VBoxLayout_main.addWidget(self.textBrowser)

        


    def initUI(self):
        setTheme(Theme.LIGHT)
        self.setObjectName("FramlessMainWIn")
        self.setStyleSheet(
            """
            #FramlessMainWIn{
                    background: rgb(255,255,255);
                                }
            QLabel{
                font : 15px 'Segoe UI';
                background-color : rgb(242,242,242);
                border-radius : 8px;
                qproperty-alignment : AlignCenter;
            }
            PushButton{
                background-color : rgb(242,242,242)
            }
            """
        )

        self.setGeometry(500,300,800,500)

        # 添加标题栏
        self.setTitleBar(StandardTitleBar(self))
        self.setWindowTitle("XM 文件解密 -- v0.1")
        self.setWindowIcon(QIcon(":/resource/Image/OIP-C(S).png"))

        self.titleBar.setAttribute(Qt.WA_StyledBackground)
        
    

