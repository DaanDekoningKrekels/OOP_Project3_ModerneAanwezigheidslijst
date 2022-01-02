import os
import sys
import datetime

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QMessageBox, QFileDialog, QInputDialog

from Windows import MainWindow
from Uitknippen import Uitknippen
from Trainen import Trainen
from Oplijsten import Oplijsten


class ModerneAanwezigheidslijst(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ModerneAanwezigheidslijst, self).__init__(parent)
        self.setupUi(self)
        self.actionStartGezichtenUitknippen.triggered.connect(self.uitknippen)
        self.actionStartTrainen.triggered.connect(self.trainen)
        self.actionStartLijstMaken.triggered.connect(self.oplijsten)

        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)  # Layout instellen in de widget
        self.scrollArea.setWidget(self.widget)  # De widget aan de scrollarea toevoegen

        self.uitknipper = Uitknippen()
        self.trainer = Trainen()
        self.oplijster = Oplijsten(self.trainer)

    def print(self, content: str):
        """
        Voegt content toe aan het MainWindow. Bv. bij het aanmaken van een Station.
        :param content: Content om toe te voegen aan het MainWindow
        """
        tekst = QLabel(str(content))
        # Ervoor zorgen dat nieuwe text aan de bovenkant wordt toegevoegd
        self.vbox.insertWidget(0, tekst)

    def uitknippen(self):
        self.print("---GEZICHTEN UITKNIPPEN---")
        # https://dev.to/threadspeed/pyqt-qinputdialog-3gf8
        # https://www.pythonguis.com/tutorials/pyqt-dialogs/
        QMessageBox.information(self, "Gezichten uitknippen", "Geef het pad naar de map met afbeeldingen in.")
        source = QFileDialog.getExistingDirectory(self, "Map met afbeeldingen om gezichten uit te knippen", "C:\\")
        print(source)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.uitknipper.findFiles(source)
        QApplication.restoreOverrideCursor()
        QMessageBox.information(self, "Gezichten uitknippen", "Geef het pad naar de map voor uitgeknipte gezichten.")
        destination = QFileDialog.getExistingDirectory(self, "Map om gezichten in te plaatsen", "C:\\")
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.uitknipper.cropFaces(destination)
        QApplication.restoreOverrideCursor()
        mededeling = f"In {destination} zitten nu de uitgeknipte bestanden."
        self.print(mededeling)
        QMessageBox.information(self, "Gezichten uitknippen", mededeling)
        mededeling = "Om deze te gebruiken voor de Trainer sorteer je de personen manueel in mappen."
        self.print(mededeling)
        QMessageBox.information(self, "Gezichten uitknippen", mededeling)
        path = os.path.realpath(destination)
        os.startfile(path)

    def trainen(self):
        self.print("---TRAINEN VAN GEZICHTSHERKENNING--")
        # antw = input("Wilt u gezichtsencodings importeren (a) of nieuwe encodings genereren (b)? a/b: ")
        # select option
        opties = ["Gezichtsencodings importeren", "Nieuwe encodings genereren"]
        item, ok = QInputDialog.getItem(self, 'getItem',
                                        'Wilt u gezichtsencodings importeren of nieuwe encodings genereren', opties, 0,
                                        False)

        if ok and item:
            if item == opties[0]:
                # Gezichtsencodings importeren
                mededeling = "Geef het pad van het face_encodings.pickle bestand."
                QMessageBox.information(self, "Gezichtsencodings importeren", mededeling)
                impmap, _ = QFileDialog.getOpenFileName(self, mededeling,
                                                        'c:\\', "Pickle files (*.pickle)")
                print(impmap)
                QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                self.trainer.import_faces(str(impmap))
            QApplication.restoreOverrideCursor()
            if item == opties[1]:
                # Nieuwe encodings genereren
                mededeling = "Geef het pad naar de map met de gesorteerde gezichten."
                QMessageBox.information(self, "Gezichten importeren", mededeling)
                gezichtenmap = QFileDialog.getExistingDirectory(self, mededeling, "C:\\")
                QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                self.trainer.train(str(gezichtenmap))
                QApplication.restoreOverrideCursor()
                mededeling = "De training is gelukt."
                self.print(mededeling)
                QMessageBox.information(self, "Klaar!", mededeling)
                antw = QMessageBox.question(self, "Gezichtsencodings exporteren?",
                                            "Wilt u de gezichtsencodings exporteren?")
                if antw == QMessageBox.StandardButton.Yes:
                    mededeling = "Geef het pad naar waar u de gezichtsencodings wilt exporteren: "
                    QMessageBox.information(self, "Gezichtsencodings exporteren", mededeling)
                    expmap = QFileDialog.getExistingDirectory(self, mededeling, "C:\\")
                    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                    self.trainer.export_faces(str(expmap))
                    QApplication.restoreOverrideCursor()
                mededeling = "De trainingdata kan nu gebruikt worden om een oplijsitng te maken."
                self.print(mededeling)
                QMessageBox.information(self, "Klaar!", mededeling)

    def oplijsten(self):
        print("---AANWEZIGEN OPLIJSTEN---")
        opties = ["Aanwezigheidslijst opstellen", "Personen op foto omcirkelen", "Beide opties"]
        keuze, ok = QInputDialog.getItem(self, 'getItem', 'Wat wilt u doen?', opties, 0, False)
        if ok and keuze:
            if keuze == opties[0] or keuze == opties[1] or keuze == opties[2]:
                mededeling = "Geef het pad naar de afbeelding met de aanwezigen"
                QMessageBox.information(self, "Afbeelding aanduiden", mededeling)
                inp_afb, _ = QFileDialog.getOpenFileName(self, mededeling,
                                                         'c:\\', "Images (*.jpg)")
            else:
                raise ValueError
            if keuze == opties[0] or keuze == opties[2]:
                mededeling = "Geef in waar u de ledenlijst wilt opslaan."
                QMessageBox.information(self, "Ledenlijst opslaan", mededeling)
                outp_csv, _ = QFileDialog.getSaveFileName(self, mededeling, "ledenlijst.csv",
                                                          "Comma-Separated Value Files (*.csv)")
                if keuze == opties[0]:
                    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                    self.oplijster.get_list(inp_afb, outp_csv, datetime.date.today())
                    QApplication.restoreOverrideCursor()
            if keuze == opties[1] or keuze == opties[2]:
                mededeling = "Geef in waar u de bewerkte afbeelding wilt opslaan."
                QMessageBox.information(self, "Ledenlijst opslaan", mededeling)
                outp_abf, _ = QFileDialog.getSaveFileName(self, mededeling, "outp.jpg",
                                                          "Images (*.jpg)")
                if keuze == opties[1]:
                    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                    self.oplijster.draw_rect(inp_afb, outp_abf, datetime.date.today())
                    QApplication.restoreOverrideCursor()
            if keuze == opties[2]:
                QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                self.oplijster.get_list_draw_rect(inp_afb, outp_abf, outp_csv, datetime.date.today())
                QApplication.restoreOverrideCursor()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ModerneAanwezigheidslijst()
    form.show()
    app.exec()
