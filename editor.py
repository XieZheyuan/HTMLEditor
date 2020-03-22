from PyQt5 import Qsci,QtGui,QtCore,QtWidgets
'''
https://www.jianshu.com/p/e5c9454e7597
'''
__author__=["Hemmelfort","Xie Zheyuan"]

class CodeWidget(Qsci.QsciScintilla):

    def __init__(self):
        super().__init__()

        self.setEolMode(self.SC_EOL_LF)    # 以\n换行
        self.setWrapMode(self.WrapWord)    # 自动换行。self.WrapWord是父类QsciScintilla的
        self.setAutoCompletionSource(self.AcsAll)  # 自动补全。对于所有Ascii字符
        self.setAutoCompletionCaseSensitivity(False)  # 自动补全大小写敏感
        self.setAutoCompletionThreshold(3)  # 输入多少个字符才弹出补全提示
        self.setFolding(True)  # 代码可折叠
        self.setFont(QtGui.QFont('Consolas', 12))  # 设置默认字体
        self.setMarginType(0, self.NumberMargin)    # 0~4。第0个左边栏显示行号
        self.setMarginLineNumbers(0, True)
        # self.setMarginsBackgroundColor(QtGui.QColor(120, 220, 180))  # 边栏背景颜色
        # self.setMarginWidth(0, 30)  # 边栏宽度
        self.setAutoIndent(True)  # 换行后自动缩进
        self.setUtf8(True)  # 支持中文字符

    def setSyntax(self):
        lexer = Qsci.QsciLexerHTML(self)
        # lexer.setDefaultFont(这里填 QFont 类型的字体)
        self.setLexer(lexer)

    def wheelEvent(self, e):
        ''' Ctrl + 滚轮 控制字体缩放 '''
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            da = e.angleDelta()
            if da.y() > 0:
                self.zoomIn(1)  # QsciScintilla 自带缩放的功能。参数是增加的字体点数
            elif da.y() < 0:
                self.zoomOut(1)
        else:
            super().wheelEvent(e)  # 留点汤给父类，不然滚轮无法翻页
