import os
import sys
import datetime

from PyQt6 import QtWidgets, QtCore
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
        self.statusbar.showMessage("Daan Dekoning Krekels | 2ITIOT | Python OOP | 2021-2022")
        # Acties toevoegen aan knoppen
        self.actionStartGezichtenUitknippen.triggered.connect(self.uitknippen)
        self.actionStartTrainen.triggered.connect(self.trainen)
        self.actionStartLijstMaken.triggered.connect(self.oplijsten)

        # Mogelijk maken om text toe te voegen aan uitputveld
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)  # Layout instellen in de widget
        self.scrollArea.setWidget(self.widget)  # De widget aan de scrollarea toevoegen

        self.uitknipper = Uitknippen(report=self)
        self.trainer = Trainen(report=self)
        self.oplijster = Oplijsten(self.trainer, report=self)

    def print(self, content: str):
        """
        Voegt content toe aan het MainWindow.
        :param content: Content om toe te voegen aan het MainWindow
        """
        tekst = QLabel(str(content))
        # Ervoor zorgen dat nieuwe text aan de bovenkant wordt toegevoegd
        self.vbox.insertWidget(0, tekst)

    def uitknippen(self):
        """
        Wordt geroepen als iemand op de Gezichten Uitknippen knop drukt.
        :return: False als er iets misgaat
        """
        self.print("---GEZICHTEN UITKNIPPEN---")
        # https://dev.to/threadspeed/pyqt-qinputdialog-3gf8
        # https://www.pythonguis.com/tutorials/pyqt-dialogs/
        QMessageBox.information(self, "Gezichten uitknippen", "Geef het pad naar de map met afbeeldingen in.")
        source = QFileDialog.getExistingDirectory(self, "Map met afbeeldingen om gezichten uit te knippen",
                                                  os.path.expanduser("~"))
        if os.path.isdir(source):
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            self.uitknipper.findFiles(source)
            QApplication.restoreOverrideCursor()
        else:
            return False
        QMessageBox.information(self, "Gezichten uitknippen", "Geef het pad naar de map voor uitgeknipte gezichten.")
        destination = QFileDialog.getExistingDirectory(self, "Map om gezichten in te plaatsen", os.path.expanduser("~"))
        if os.path.isdir(destination):
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            self.uitknipper.cropFaces(destination)
            QApplication.restoreOverrideCursor()
        else:
            return False
        mededeling = f"In {destination} zitten nu de uitgeknipte bestanden."
        self.print(mededeling)
        QMessageBox.information(self, "Gezichten uitknippen", mededeling)
        mededeling = "Om deze te gebruiken voor de Trainer sorteer je de personen manueel in mappen."
        self.print(mededeling)
        QMessageBox.information(self, "Gezichten uitknippen", mededeling)
        path = os.path.realpath(destination)
        os.startfile(path)

    def trainen(self):
        """
        Wordt geroepen als iemand op de Trainen op Gezichten knop drukt.
        :return: False als er iets misgaat
        """
        self.print("---TRAINEN VAN GEZICHTSHERKENNING--")
        opties = ["Gezichtsencodings importeren", "Nieuwe encodings genereren"]
        item, ok = QInputDialog.getItem(self, 'getItem',
                                        'Wilt u gezichtsencodings importeren of nieuwe encodings genereren', opties, 0,
                                        False)

        if ok and item:
            if item == opties[0]:
                # Gezichtsencodings importeren
                mededeling = "Geef het pad van het face_encodings.pickle bestand."
                QMessageBox.information(self, "Gezichtsencodings importeren", mededeling)
                impfile, _ = QFileDialog.getOpenFileName(self, mededeling,
                                                         os.path.expanduser("~"), "Pickle files (*.pickle)")
                print(impfile)
                if os.path.isfile(impfile):
                    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                    self.trainer.import_faces(impfile)
                    QApplication.restoreOverrideCursor()
                else:
                    return False
            if item == opties[1]:
                # Nieuwe encodings genereren
                mededeling = "Geef het pad naar de map met de gesorteerde gezichten."
                QMessageBox.information(self, "Gezichten importeren", mededeling)
                gezichtenmap = QFileDialog.getExistingDirectory(self, mededeling, os.path.expanduser("~"))
                if os.path.isdir(gezichtenmap):
                    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                    self.trainer.train(str(gezichtenmap))
                    QApplication.restoreOverrideCursor()
                    mededeling = "De training is gelukt."
                    self.print(mededeling)
                    QMessageBox.information(self, "Klaar!", mededeling)
                else:
                    return False
                antw = QMessageBox.question(self, "Gezichtsencodings exporteren?",
                                            "Wilt u de gezichtsencodings exporteren?")
                if antw == QMessageBox.StandardButton.Yes:
                    mededeling = "Geef het pad naar waar u de gezichtsencodings wilt exporteren: "
                    QMessageBox.information(self, "Gezichtsencodings exporteren", mededeling)
                    expmap = QFileDialog.getExistingDirectory(self, mededeling, os.path.expanduser("~"))
                    if os.path.isdir(expmap):
                        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                        self.trainer.export_faces(expmap)
                        QApplication.restoreOverrideCursor()
                    else:
                        return False
                mededeling = "De trainingdata kan nu gebruikt worden om een oplijsitng te maken."
                self.print(mededeling)
                QMessageBox.information(self, "Klaar!", mededeling)

    def oplijsten(self):
        """
        Wordt geroepen als iemand op de Aanwezigheidslijst Maken knop drukt.
        :return: False als er iets misgaat
        """
        self.print("---AANWEZIGEN OPLIJSTEN---")
        if len(self.trainer.known_names) == 0:
            mededeling = "Train of importeer eerst gezichten!"
            self.print(mededeling)
            QMessageBox.warning(self, "Geen gezichtsencodings ingeladen!", mededeling)
            return False
        opties = ["Aanwezigheidslijst opstellen", "Personen op foto omcirkelen", "Beide opties"]
        keuze, ok = QInputDialog.getItem(self, 'getItem', 'Wat wilt u doen?', opties, 0, False)
        if ok and keuze:
            if keuze == opties[0] or keuze == opties[1] or keuze == opties[2]:
                # Bij alle opties:
                datum, ok = self._datumvenster()
                if not ok:
                    return False

                mededeling = "Geef het pad naar de afbeelding met de aanwezigen"
                QMessageBox.information(self, "Afbeelding aanduiden", mededeling)
                inp_afb, _ = QFileDialog.getOpenFileName(self, mededeling,
                                                         os.path.expanduser("~"), "Images (*.jpg)")
                if not os.path.isfile(inp_afb):
                    return False
            else:
                raise ValueError
            if keuze == opties[0] or keuze == opties[2]:
                # Bij Aanwezigheidslijst of Beide opties
                mededeling = "Geef in waar u de ledenlijst wilt opslaan."
                QMessageBox.information(self, "Ledenlijst opslaan", mededeling)
                outp_csv, _ = QFileDialog.getSaveFileName(self, mededeling, "ledenlijst.csv",
                                                          "Comma-Separated Value Files (*.csv)")
                if outp_csv == '':
                    return False
                if keuze == opties[0]:
                    # Enkel bij Aanwezigheidslijst
                    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                    self.oplijster.get_list(inp_afb, outp_csv, datetime.date(datum.year(), datum.month(), datum.day()))
                    QApplication.restoreOverrideCursor()
            if keuze == opties[1] or keuze == opties[2]:
                # Bij Omcirkelen of Beide opties
                mededeling = "Geef in waar u de bewerkte afbeelding wilt opslaan."
                QMessageBox.information(self, "Ledenlijst opslaan", mededeling)
                outp_abf, _ = QFileDialog.getSaveFileName(self, mededeling, "outp.jpg",
                                                          "Images (*.jpg)")
                if outp_abf == '':
                    return False
                if keuze == opties[1]:
                    # Enkel bij Omcirkelen
                    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                    self.oplijster.draw_rect(inp_afb, outp_abf, datetime.date(datum.year(), datum.month(), datum.day()))
                    QApplication.restoreOverrideCursor()
            if keuze == opties[2]:
                # Enkel bij Beide opties
                QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                self.oplijster.get_list_draw_rect(inp_afb, outp_abf, outp_csv,
                                                  datetime.date(datum.year(), datum.month(), datum.day()))
                QApplication.restoreOverrideCursor()

    def _datumvenster(self):
        dateedit = QtWidgets.QDateEdit(calendarPopup=True)
        # self.menuBar().setCornerWidget(self.dateedit, QtCore.Qt.Corner.TopLeftCorner)
        dateedit.setDateTime(QtCore.QDateTime.currentDateTime())

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Datum van vergadering")
        dlg.setText("Geef de datum van de vergadering in.")
        dlg.layout().addWidget(dateedit)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        button = dlg.exec()
        ok = False
        if button == QMessageBox.StandardButton.Ok:
            ok = True

        return dateedit.date(), ok


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ModerneAanwezigheidslijst()
    form.show()
    app.exec()
