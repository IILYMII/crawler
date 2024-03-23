from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import sys
from GUI import Ui_MainWindow
import crawler

# class workThread(QThread):
#     sig = pyqtSignal(int)
#     def __init__(self):
#         super().__init__()


class mainWindowControl(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupControl() 

    def setupControl(self):
        self.ui.dirButton.clicked.connect(self.openFolder)
        self.ui.searchButton.clicked.connect(self.searchmanga)
        self.ui.downloadButton.clicked.connect(self.downloadStart)
        self.ui.autoMKDir.clicked.connect(self.checkAutoMKDir)
        self.ui.mutiProcess.clicked.connect(self.checkThreadPool)

    def openFolder(self):
        foldername = QFileDialog.getExistingDirectory(self, 'Open folder', "./")
        self.ui.dirPosition.setText(foldername)
        crawl._dirBase = foldername

    def checkThreadPool(self):
        crawl._isUsingThreadPool ^= 1

    def checkAutoMKDir(self):
        crawl._mkdir ^= 1
        
    def searchmanga(self):
        number = self.ui.numberInput.text()
        crawl.webAddress(number)
        self.ui.mangaLabel.setText(f'{crawl._dirName}')
        if crawl._dirName == '無法取得內容，請確認是否存在或檢查userInfo內的資料(可能過期，須更新)':
            self.ui.downloadButton.setEnabled(False)
            self.showimg(True)
        else:
            self.showimg()
            self.ui.downloadButton.setEnabled(True)

    def showimg(self , nf = False):
        if not nf:
            crawl._dlMethod()
        img = QPixmap('./titlePage.jpg' if not nf else './notFound.jpg')
        img = img.scaled(260 , 340)
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(img)
        self.ui.graphicsView.setScene(scene)

    # def showDownloadProcess(self , curprocess):
    #     self.ui.progressBar.setValue(curprocess)

    def downloadStart(self):
        # self.ui.progressBar.setEnabled(True)
        # self.ui.progressBar.setMaximum(crawl._b)
        # self.thread = workThread()
        # self.thread.sig.connect(self.showDownloadProcess)
        crawl.doDownload()
        if crawl._error:
            self.ui.mangaLabel.setText("發生錯誤")
        else:
            self.ui.mangaLabel.setText(f'{crawl._dirName} \n\n ==== 已完成下載 ====')
        self.ui.downloadButton.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    crawl = crawler.crawl()
    window = mainWindowControl()
    window.show()
    sys.exit(app.exec_())