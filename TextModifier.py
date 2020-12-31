from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QListWidget, QRadioButton
from PyQt5.QtWidgets import QAbstractItemView
import os
import ntpath

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Nesting Contour")
        Top=500; Left=200; Width=530; Hight = 600
        self.setGeometry(Top, Left, Width, Hight)
        self.setMinimumSize(Width, Hight)
        # -------
        self.lswFiles = QListWidget()
        self.lswFiles.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # -------
        vbxLeft = QVBoxLayout()
        vbxLeft.addWidget(self.lswFiles)
        # -------
        self.btnBrowse = QPushButton('Browse')
        self.btnBrowse.clicked.connect(self.Browse)
        # -------
        self.btnDelete = QPushButton('Delete')
        self.btnDelete.clicked.connect(self.Delete)
        # -------
        self.btnDelAll = QPushButton('Delete All')
        self.btnDelAll.clicked.connect(self.DeleteAll)
        # -------
        self.btnSortAZ = QPushButton('Sort A-Z')
        self.btnSortAZ.clicked.connect(self.SortAZ)
        # -------
        vbxRite = QVBoxLayout()
        vbxRite.addWidget(self.btnBrowse)
        vbxRite.addWidget(self.btnDelete)
        vbxRite.addWidget(self.btnDelAll)
        vbxRite.addWidget(self.btnSortAZ)
        vbxRite.addStretch(1)
        # -------
        hbxUppr = QHBoxLayout()
        hbxUppr.addLayout(vbxLeft)
        hbxUppr.addLayout(vbxRite)
        # -------
        self.rdoOvrwrt = QRadioButton('Overwrite Existing Files')
        self.rdoOvrwrt.clicked.connect(self.Overwrit)
        # -------
        self.rdoCreate = QRadioButton('Create New')
        self.rdoCreate.setChecked(True)
        self.rdoCreate.clicked.connect(self.Create)
        # -------
        self.btnSelect = QPushButton('Select Output Location')
        self.btnSelect.clicked.connect(self.select_output_url)
        # -------
        hbxType = QHBoxLayout()
        hbxType.addWidget(self.rdoOvrwrt)
        hbxType.addWidget(self.rdoCreate)
        hbxType.addWidget(self.btnSelect)
        hbxType.addStretch(1)
        # -------
        self.output_url = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        lblOutput = QLabel('Output Location: ')
        self.lblOutUrl = QLabel(self.output_url)
        # -------
        self.btnExcute = QPushButton('Execute')
        self.btnExcute.clicked.connect(self.sp_detector_write_new)
        # -------
        hbxCntr = QHBoxLayout()
        hbxCntr.addWidget(self.btnExcute)
        hbxCntr.addStretch(1)
        # -------
        frmBttm = QFormLayout()
        frmBttm.addRow(hbxType)
        frmBttm.addRow(lblOutput, self.lblOutUrl)
        frmBttm.addRow(hbxCntr)
        # -------
        vbxMain = QVBoxLayout()
        vbxMain.addLayout(hbxUppr)
        vbxMain.addLayout(frmBttm)
        # -------
        self.setLayout(vbxMain)

    def RetrieveDataFromQList(self):
        self.list_data = []
        for i in range(self.lswFiles.count()):
            self.list_data.append(self.lswFiles.item(i).text())

    @pyqtSlot()
    def Browse(self):
        url = QFileDialog.getOpenFileNames(self, 'Open File', "", "All Files(*);;*txt;;*hop")

        for item in url[0]:
            if not self.lswFiles.findItems(item, Qt.MatchFixedString | Qt.MatchCaseSensitive):
                self.lswFiles.addItem(item)


    @pyqtSlot()
    def Delete(self):
        index = self.lswFiles.currentRow()
        self.lswFiles.takeItem(index)
        print("PRESSED DELETE")

    @pyqtSlot()
    def DeleteAll(self):
        self.lswFiles.clear()

    @pyqtSlot()
    def SortAZ(self):
        self.lswFiles.sortItems()

    @pyqtSlot()
    def Overwrit(self):
        if self.rdoOvrwrt.isChecked():
            self.btnExcute.clicked.disconnect()
            self.btnExcute.clicked.connect(self.sp_detecor_overwrte)
            self.btnSelect.setEnabled(False)


    @pyqtSlot()
    def Create(self):
        if self.rdoCreate.isChecked():
            self.btnExcute.clicked.disconnect()
            self.btnExcute.clicked.connect(self.sp_detector_write_new)
            self.btnSelect.setEnabled(True)

    def sp_detecor_overwrte(self):
        self.RetrieveDataFromQList()
        for i in self.list_data:
            with open(i, 'r') as hop_list:
                lines_list = hop_list.readlines()

            line_indexing = []
            for k in range(len(lines_list)):
                if "SP (" in lines_list[k]:
                    line_indexing.append(k)

            if len(line_indexing) > 0:
                lines_list.insert(line_indexing[-1], "CALL BN_NestKontur ()\n")
                lines_list.insert(line_indexing[-1], "CALL BN_TrennerInnenAussen ()\n")

            file_rewrite = open(i, "w")
            for j in lines_list:
                file_rewrite.write(j)

            file_rewrite.close()

        self.final_message_box()
        self.lswFiles.clear()


    def sp_detector_write_new(self):
        self.RetrieveDataFromQList()
        for i in self.list_data:
            self.file_name = ntpath.basename(i)

            file = open(i, "r")
            file_list = file.readlines()
            file.close()

            sp_line_indexing = []
            for k in range(len(file_list)):
                if "SP (" in file_list[k]:
                    sp_line_indexing.append(k)

            if len(sp_line_indexing) > 0:
                file_list.insert(sp_line_indexing[-1], "CALL BN_NestKontur ()\n")
                file_list.insert(sp_line_indexing[-1], "CALL BN_TrennerInnenAussen ()\n")

            self.absolute_final_path = self.output_url + "\\" + self.file_name

            new_file = open(self.absolute_final_path, "a")

            for j in file_list:
                new_file.write(j)

            new_file.close()

        self.final_message_box()
        self.lswFiles.clear()

    @pyqtSlot()
    def select_output_url(self):
        self.output_url = QFileDialog.getExistingDirectory(self)
        self.lblOutUrl.clear()
        self.lblOutUrl.setText(self.output_url)


    def final_message_box(self):
        self.msgbox = QMessageBox(self)
        self.msgbox.setWindowTitle("Nesting Contour")
        box_text = "Process has been successfully accomplished\n" + str(len(self.list_data)) + \
                   " files have been exported to: " + self.output_url
        self.msgbox.setText(box_text)
        self.msgbox.resize(300, 400)
        self.msgbox.exec()


if __name__ == "__main__":
    MainEvntThred = QApplication([])

    MainApplication = Window()
    MainApplication.show()

    MainEvntThred.exec()
