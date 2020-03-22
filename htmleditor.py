'''
HTML EDITOR MAIN PROGRAM
COPYRIGHT (C) XIE ZHEYUAN
'''
__author__ = 'Xie Zheyuan'
from PyQt5 import QtCore,QtGui,QtWidgets
from Ribbon import RibbonButton,RibbonWidget
import editor
from sys import argv

class HTMLEditor(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(HTMLEditor, self).__init__(parent=parent)
        self.setWindowTitle("HTML Editor")
        self.setDockNestingEnabled(True)

        #File Menu
        self.newFile=QtWidgets.QAction(QtGui.QIcon("icons/new.ico"),"New",self)
        self.openFile=QtWidgets.QAction(QtGui.QIcon("icons/open.ico"),"Open",self)
        self.saveFile=QtWidgets.QAction(QtGui.QIcon("icons/save.ico"),"Save",self)
        self.saveAsFile=QtWidgets.QAction(QtGui.QIcon("icons/saveas.ico"),"Save As",self)
        self.exitAction=QtWidgets.QAction(QtGui.QIcon("icons/exit.ico"),"Exit",self)

        #Insert Inline Menu
        self.insertBold=QtWidgets.QAction(QtGui.QIcon("icons/bold.ico"),"Bold",self)
        self.insertBold.triggered.connect(self.insertSomething("<b>...</b>"))
        self.insertItalic=QtWidgets.QAction(QtGui.QIcon("icons/italic.ico"),"Italic",self)
        self.insertItalic.triggered.connect(self.insertSomething("<i>...</i>"))
        self.insertUnderline=QtWidgets.QAction(QtGui.QIcon("icons/underline.ico"),"Underline",self)
        self.insertUnderline.triggered.connect(self.insertSomething("<u>...</u>"))
        self.insertDeleteline=QtWidgets.QAction(QtGui.QIcon("icons/deleteline.ico"),"DeleteLine",self)
        self.insertDeleteline.triggered.connect(self.insertSomething("<del>...</del>"))
        self.insertSpan=QtWidgets.QAction(QtGui.QIcon("icons/span.ico"),"Span Element",self)
        self.insertSpan.triggered.connect(self.insertSomething("<span>...</span>"))
        self.insertCodeElement=QtWidgets.QAction(QtGui.QIcon("icons/code.ico"),"Code Element",self)
        self.insertCodeElement.triggered.connect(self.insertSomething("<code>...</code>"))
        self.insertLink=QtWidgets.QAction(QtGui.QIcon("icons/link.ico"),"Hyperlink",self)
        self.insertLink.triggered.connect(self.insertLink_action)

        #Insert Block Menu
        self.insertDiv=QtWidgets.QAction(QtGui.QIcon("icons/div.ico"),"Div Element",self)
        self.insertDiv.triggered.connect(self.insertSomething("<div>...</div>"))

        self.insertLine=QtWidgets.QAction(QtGui.QIcon("icons/hr.ico"),"Horizon",self)
        self.insertLine.triggered.connect(self.add_const())

        self.insertNextLine=QtWidgets.QAction(QtGui.QIcon("icons/nextline.ico"),"Line breaks",self)
        self.insertNextLine.triggered.connect(self.add_const("<br />"))
        self.insertOl=QtWidgets.QAction(QtGui.QIcon("icons/ol.ico"),"Ordered",self)
        self.bind(self.insertOl,self.add_const("<ol>\n\n</ol>"))
        self.insertUl=QtWidgets.QAction(QtGui.QIcon("icons/ul.ico"),"Disordered",self)
        self.bind(self.insertUl,self.add_const("<ul>\n</ul>"))
        self.insertListItem=QtWidgets.QAction(QtGui.QIcon("icons/list-item.ico"),"Item",self)
        self.bind(self.insertListItem,self.insertSomething("<li>...</li>\n"))
        self.insertTable=QtWidgets.QAction(QtGui.QIcon("icons/table.ico"),"Normal",self)
        self.insertTableWithoutBroder=QtWidgets.QAction(QtGui.QIcon("icons/table.ico"),"No border",self)
        self.insertTableLine=QtWidgets.QAction(QtGui.QIcon("icons/table.ico"),"Line",self)
        self.insertTableCeil=QtWidgets.QAction(QtGui.QIcon("icons/table.ico"),"Ceil",self)
        self.insertPreCode=QtWidgets.QAction(QtGui.QIcon("icons/code.ico"),"PRE Code",self)
        self.insertAddress=QtWidgets.QAction(QtGui.QIcon("icons/url.ico"),"Address",self)

        self._ribbon=RibbonWidget.RibbonWidget(self)
        self.addToolBar(self._ribbon)
        self.init_ribbon()
        self.editor=editor.CodeWidget()
        self.setCentralWidget(self.editor)
    def init_ribbon(self):
        file_tab=self._ribbon.add_ribbon_tab("Start")
        file_pane=file_tab.add_ribbon_pane("File")
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.newFile,True))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.openFile,True))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.saveFile,True))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.saveAsFile,True))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.exitAction,True))
        insert_inline_tab=self._ribbon.add_ribbon_tab("Inline")
        text_pane=insert_inline_tab.add_ribbon_pane("Text")
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertBold,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertItalic,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertUnderline,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertDeleteline,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertSpan,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertCodeElement,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertLink,True))
        insert_block_tab=self._ribbon.add_ribbon_tab("Block")
        separating_pane=insert_block_tab.add_ribbon_pane("Separating elements")
        separating_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertDiv,True))
        separating_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertLine,True))
        separating_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertNextLine,True))
        list_pane=insert_block_tab.add_ribbon_pane("List")
        list_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertOl,True))
        list_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertUl,True))
        list_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertListItem,True))
        table_pane=insert_block_tab.add_ribbon_pane("Table")
        table_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertTable,True))
        table_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertTableWithoutBroder,True))
        table_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertTableLine,True))
        table_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertTableCeil,True))
        muti_text_pane=insert_block_tab.add_ribbon_pane("Block Text")
        muti_text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertPreCode,True))
        muti_text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertAddress,True))
    def insertSomething(self,sth):
        def foo():
            sth2=QtWidgets.QInputDialog.getText(self,"HTML Editor","Input An Label:",text="...")
            if sth2[1] != True:
                return
            else:
                sth2=sth2[0]
            sth3=sth.replace("...",sth2)

            self.editor.insert(sth3)
        return foo
    def insertLink_action(self):
        url=QtWidgets.QInputDialog.getText(self,"HTML Editor","Input the Hyperlink URL",text="about:blank")
        if url[1] != True:
            return
        else:
            url=url[0]
        text=QtWidgets.QInputDialog.getText(self,"HTML Editor","Input the Hyperlink Show Text",text="...")
        if text[1] != True:
            return
        else:
            text=text[0]
        link="<a href=\""+url+"\">"+text+"</a>"
        self.editor.insert(link)
    def add_const(self,s="<hr />"):
        def foo():
            self.editor.insert(s)
        return foo
    def bind(self,action:QtWidgets.QAction,futc):
        action.triggered.connect(futc)
if __name__ == "__main__":
    app=QtWidgets.QApplication(argv)
    win=HTMLEditor()
    if "fullscreen" in argv or "full_screen" in argv :
        win.showFullScreen()
    elif "minimum" in argv:
        win.showMinimized()
    elif "normal" in argv:
        win.showNormal()
    else:
        win.showMaximized()
    __import__("sys").exit(app.exec_())