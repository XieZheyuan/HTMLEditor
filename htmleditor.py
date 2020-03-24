'''
HTML EDITOR MAIN PROGRAM
COPYRIGHT (C) XIE ZHEYUAN
'''
__author__ = 'Xie Zheyuan'
from PyQt5 import QtCore,QtGui,QtWidgets
from Ribbon import RibbonButton,RibbonWidget
import editor,il8nlib
from sys import argv
i=il8nlib.Il8n()
HTML_FILTER="HTML Page(*.html *.htm *.shtml *.xhtml *.mht *.mhtml)"
def opfile(fpath):
    obj=open(fpath,'r')
    txt=obj.read(
    )
    obj.close()
    return txt
def writefile(fpath,data):
    obj=open(fpath,'w')
    obj.write(data)
    obj.close()
class HTMLEditor(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(HTMLEditor, self).__init__(parent=parent)
        self.setWindowTitle(i._("title"))
        self.setDockNestingEnabled(True)
        self.fn=None
        #File Menu
        self.newFileAction=QtWidgets.QAction(QtGui.QIcon("icons/new.ico"),i._("newFileActionName"),self)
        self.bind(self.newFileAction,self.newFile)
        self.openFileAction=QtWidgets.QAction(QtGui.QIcon("icons/open.ico"),i._("openFileActionName"),self)
        self.bind(self.openFileAction,self.openFile)
        self.saveFileAction=QtWidgets.QAction(QtGui.QIcon("icons/save.ico"),i._("saveFileActionName"),self)
        self.bind(self.saveFileAction,self.save)
        self.saveAsFileAction=QtWidgets.QAction(QtGui.QIcon("icons/saveas.ico"),i._("saveasFileAction"),self)
        self.bind(self.saveFileAction,self.saveas)
        self.exitAction=QtWidgets.QAction(QtGui.QIcon("icons/exit.ico"),i._("exitAction"),self)
        self.bind(self.exitAction,self.quit)

        #Insert Inline Menu
        self.insertBold=QtWidgets.QAction(QtGui.QIcon("icons/bold.ico"),i._("makeBoldActionName"),self)
        self.insertBold.triggered.connect(self.insertSomething("<b>...</b>"))
        self.insertItalic=QtWidgets.QAction(QtGui.QIcon("icons/italic.ico"),i._("makeItalicActionName"),self)
        self.insertItalic.triggered.connect(self.insertSomething("<i>...</i>"))
        self.insertUnderline=QtWidgets.QAction(QtGui.QIcon("icons/underline.ico"),i._("makeUnderlineActionName"),self)
        self.insertUnderline.triggered.connect(self.insertSomething("<u>...</u>"))
        self.insertDeleteline=QtWidgets.QAction(QtGui.QIcon("icons/deleteline.ico"),i._("makeDeleteLineActionName"),self)
        self.insertDeleteline.triggered.connect(self.insertSomething("<del>...</del>"))
        self.insertSpan=QtWidgets.QAction(QtGui.QIcon("icons/span.ico"),i._("addSpanActionName"),self)
        self.insertSpan.triggered.connect(self.insertSomething("<span>...</span>"))
        self.insertCodeElement=QtWidgets.QAction(QtGui.QIcon("icons/code.ico"),i._("addCodeElementActionName"),self)
        self.insertCodeElement.triggered.connect(self.insertSomething("<code>...</code>"))
        self.insertLink=QtWidgets.QAction(QtGui.QIcon("icons/link.ico"),i._("addHyperlinkElement"),self)
        self.insertLink.triggered.connect(self.insertLink_action)
        self.insertParagraph=QtWidgets.QAction(QtGui.QIcon("icons/Paragraph.ico"),i._("makeParagraphActionElement"),self)
        self.bind(self.insertParagraph,self.insertSomething("<p>...</p>"))
        #Insert Block Menu
        self.insertDiv=QtWidgets.QAction(QtGui.QIcon("icons/div.ico"),i._("makeDivActionName"),self)
        self.insertDiv.triggered.connect(self.insertSomething("<div>...</div>"))

        self.insertLine=QtWidgets.QAction(QtGui.QIcon("icons/hr.ico"),i._("AddLineActionName"),self)
        self.insertLine.triggered.connect(self.add_const())

        self.insertNextLine=QtWidgets.QAction(QtGui.QIcon("icons/nextline.ico"),i._("NewLineAction"),self)
        self.insertNextLine.triggered.connect(self.add_const("<br />"))
        self.insertOl=QtWidgets.QAction(QtGui.QIcon("icons/ol.ico"),"Ordered",self)
        self.bind(self.insertOl,self.add_const("<ol>\n\n</ol>"))
        self.insertUl=QtWidgets.QAction(QtGui.QIcon("icons/ul.ico"),"Disordered",self)
        self.bind(self.insertUl,self.add_const("<ul>\n\n</ul>"))
        self.insertListItem=QtWidgets.QAction(QtGui.QIcon("icons/list-item.ico"),"Item",self)
        self.bind(self.insertListItem,self.insertSomething("<li>...</li>\n"))
        self.insertTable=QtWidgets.QAction(QtGui.QIcon("icons/table.ico"),"Normal",self)
        self.bind(self.insertTable,self.add_const("<table border>\n\n</table>"))
        self.insertTableWithoutBroder=QtWidgets.QAction(QtGui.QIcon("icons/table.ico"),"No border",self)
        self.bind(self.insertTableWithoutBroder,self.add_const("<table>\n\n</table>"))
        self.insertTableLine=QtWidgets.QAction(QtGui.QIcon("icons/table.ico"),"Line",self)
        self.bind(self.insertTableLine,self.add_const("<tr>\t</tr>"))
        self.insertTableCeil=QtWidgets.QAction(QtGui.QIcon("icons/table.ico"),"Ceil",self)
        self.bind(self.insertTableCeil,self.insertSomething("<td>...</td>"))
        self.insertPreCode=QtWidgets.QAction(QtGui.QIcon("icons/code.ico"),"PRE Code",self)
        self.bind(self.insertPreCode,self.add_const("<pre>\n\n</pre>"))
        self.insertAddress=QtWidgets.QAction(QtGui.QIcon("icons/url.ico"),"Address",self)
        self.bind(self.insertAddress,self.insertSomething("<address>...</address>"))

        self._ribbon=RibbonWidget.RibbonWidget(self)
        self.addToolBar(self._ribbon)
        self.init_ribbon()
        self.editor=editor.CodeWidget()
        self.setCentralWidget(self.editor)
    def init_ribbon(self):
        file_tab=self._ribbon.add_ribbon_tab(i._("startMenuName"))
        file_pane=file_tab.add_ribbon_pane(i._("filePaneName"))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.newFileAction,True))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.openFileAction,True))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.saveFileAction,True))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.saveAsFileAction,True))
        file_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.exitAction,True))
        insert_inline_tab=self._ribbon.add_ribbon_tab(i._("inlineMenuName"))
        text_pane=insert_inline_tab.add_ribbon_pane(i._("inlineTextPaneName"))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertBold,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertItalic,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertUnderline,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertDeleteline,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertSpan,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertCodeElement,True))
        text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertLink,True))
        # text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertParagraph,True))
        insert_block_tab=self._ribbon.add_ribbon_tab(i._("blockMenuName"))
        # block_text_pane=insert_block_tab.add_ribbon_pane("Block Text")
        # block_text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertParagraph,True))
        separating_pane=insert_block_tab.add_ribbon_pane(i._("Separating"))
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
        muti_text_pane.add_ribbon_widget(RibbonButton.RibbonButton(self,self.insertParagraph,True))
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
    def newFile(self):
        self.editor.clear()
        self.fn=None
        self.upgradeFN()
    def openFile(self):
        fpath=QtWidgets.QFileDialog.getOpenFileName(self,"Open the HTML File",filter=HTML_FILTER)[0]
        if fpath == "" or fpath == None:
            return False
        txt=opfile(fpath)
        print(txt)
        self.editor.clear()
        self.editor.setText(txt)
        self.fn=fpath
        self.upgradeFN()
    def save(self):
        if self.fn == None:
            fn=QtWidgets.QFileDialog.getSaveFileName(self,"Save to HTML",filter=HTML_FILTER)[0]
            if fn == "" or fn == None:
                return False
            writefile(fn,self.editor.text())
            self.fn=fn
        else:
            writefile(self.fn,self.editor.text())
    def saveas(self):
        fn = QtWidgets.QFileDialog.getSaveFileName(self, "Save to HTML", filter=HTML_FILTER)[0]
        if fn == "" or fn == None:
            return False
        writefile(fn, self.editor.text())
        self.upgradeFN()
    def quit(self):
        self.close()
        exit(0)
    def upgradeFN(self):
        if self.fn == None:
            self.setWindowTitle("HTMLEditor")
        self.setWindowTitle("%s-HTMLEditor"%self.fn)
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
