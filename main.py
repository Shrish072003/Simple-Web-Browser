import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

        # MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # ADD TAB WIGDETS TO DISPLAY WEB TABS
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # ADD TAB CLOSE EVENT LISTENER
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # ADD ACTIVE TAB CHANGE EVENT LISTENER
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # SET WINDOW TITTLE AND ICON
        self.setWindowTitle("Open Browser")
        self.setWindowIcon(QIcon(os.path.join('logo.png')))
        # ADD NAVIGATION TOOLBAR
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(18, 18))
        self.addToolBar(navtb)

        # ADD BUTTONS TO NAVIGATION TOOLBAR
        # PREVIOUS WEB PAGE BUTTON
        back_btn = QAction(QIcon(os.path.join('back.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)
        # NAVIGATE TO PREVIOUS PAGE
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())




        # NEXT WEB PAGE BUTTON
        next_btn = QAction(QIcon(os.path.join('forward.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)
        # NAVIGATE TO NEXT WEB PAGE
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())




        # REFRESH WEB PAGE BUTTON
        reload_btn = QAction(QIcon(os.path.join('reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        navtb.addAction(reload_btn)
        # RELOAD WEB PAGE
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())







        # ADD SEPARATOR TO NAVIGATION BUTTONS
        navtb.addSeparator()

        # ADD LABEL ICON TO SHOW THE SECURITY STATUS OF THE LOADED URL
        self.httpsicon = QLabel()  
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))
        navtb.addWidget(self.httpsicon)

        # ADD LINE EDIT TO SHOW AND EDIT URLS
        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        # LOAD URL WHEN ENTER BUTTON IS PRESSED
        self.urlbar.returnPressed.connect(self.navigate_to_url)
      



        # ADD STYLESHEET TO CUSTOMIZE YOUR WINDOWS
        # STYLESHEET (DARK MODE)
        self.setStyleSheet("""QWidget{
            margin-top:3px;
           background: #202124;
           border-bottom-right-radius: 8px ;
           color: rgb(255, 255, 255);
        }
        QTabWidget::pane { /* The tab widget frame */
            background:#202124;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QToolButton {
            background: #202124;
border-radius: 8px ;
            padding: 3px;
            margin-right: 3px;
        }
        QLabel {
            background: #35363A;
border-radius: 8px ;
            padding: 3px;
            margin-right: 3px;
        }
        QTabBar::tab {
            background: #35363A;
box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
border-radius: 8px ;
            padding: 8px;
            margin-top: 2px;
            margin-right: 0px;
border-bottom-right-radius: 0px ;
border-bottom-left-radius: 0px ;
        }


        QLineEdit {
            border: 0px;
            border-radius: 13px;
            padding: 4px;
            font-size:15px;
            background: #35363A;
        }
        QLineEdit:hover {
            background: #35363A;
border-radius: 13px;

        }
        QPushButton{
            background: #202124;
border-radius: 8px ;
        }""")


        new_tab_btn = QAction(QIcon(os.path.join('add.png')), "New Tab", self)
        new_tab_btn.setStatusTip("Open a new tab")
        navtb.addAction(new_tab_btn)
        # ADD NEW TAB
        new_tab_btn.triggered.connect(lambda _: self.add_new_tab())


        # LOAD DEFAULT HOME PAGE (GOOLE.COM)
        #url = http://www.google.com,
        #label = Homepage
        self.add_new_tab(QUrl('http://www.google.com'), 'Loading')

        # SHOW MAIN WINDOW
        self.show()

        # ADD NEW WEB TAB
    def add_new_tab(self, qurl=None, label="New Tab"):
        # Check if url value is blank
        if qurl is None:
            qurl = QUrl('http://www.google.com')#open direct google

        # Load the passed url
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # ADD THE WEB PAGE TAB
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        
        # ADD BROWSER EVENT LISTENERS
        # On URL change
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        # On loadfinished
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))


        # CLOSE TABS 
    def close_current_tab(self, i):
        self.tabs.removeTab(i)


        # UPDATE URL TEXT WHEN ACTIVE TAB IS CHANGED
    def update_urlbar(self, q, browser=None):
        #q = QURL
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return
        # URL Schema
        if q.scheme() == 'https':
        # If schema is https change icon to locked padlock to show that the webpage is secure
            self.httpsicon.setPixmap(QPixmap(os.path.join('lock.png')))

        else:
        # If schema is not https change icon to locked padlock to show that the webpage is unsecure
            self.httpsicon.setPixmap(QPixmap(os.path.join('unlock.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)



        # ACTIVE TAB CHANGE ACTIONS
    def current_tab_changed(self, i):
        # GET CURRENT TAB URL
        qurl = self.tabs.currentWidget().url()
        # UPDATE URL TEXT
        self.update_urlbar(qurl, self.tabs.currentWidget())
        


        # NAVIGATE TO PASSED URL
    def navigate_to_url(self):  # Does not receive the Url
        # GET URL TEXT
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
        # pass http as default url schema
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

       

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MainWindow()
    Form.show()
    sys.exit(app.exec_())
