import datetime

from Uitknippen import Uitknippen
from Trainen import Trainen
from Oplijsten import Oplijsten


class Programma():
    def __init__(self):
        self.uitknipper = Uitknippen()
        self.trainer = Trainen()
        self.oplijster = Oplijsten(self.trainer)

    def uitknippen(self):
        print("---GEZICHTEN UITKNIPPEN---")
        source = input("Geef het pad naar de map met afbeeldingen in: ")
        self.uitknipper.findFiles(str(source))
        destination = input("Geef het pad naar de map voor uitgeknipte gezichten: ")
        self.uitknipper.cropFaces(str(destination))
        print(f"In {destination} zitten nu de uitgeknipte bestanden.")
        print("Om deze te gebruiken voor de Trainer sorteer je de personen manueel in mappen.")

    def trainen(self):
        print("---TRAINEN VAN GEZICHTSHERKENNING--")
        antw = input("Wilt u gezichtsencodings importeren (a) of nieuwe encodings genereren (b)? a/b: ")

        if antw == 'a':
            impmap = input("Geef het pad van het face_encodings.pickle bestand: ")
            self.trainer.import_faces(str(impmap))
        if antw == 'b':
            gezichtenmap = input("Geef het pad naar de map met de gesorteerde gezichten: ")
            self.trainer.train(str(gezichtenmap))
            print("De training is gelukt.")
            antw = input("Wilt u de gezichtsencodings exporteren? j/n: ")
            if antw == 'j':
                expmap = input("Geef het pad naar waar u de gezichtsencodings wilt exporteren: ")
                self.trainer.export_faces(str(expmap))
        print("De trainingdata kan nu gebruikt worden om een oplijsitng te maken.")

    def oplijsten(self):
        print("---AANWEZIGEN OPLIJSTEN---")
        print("a: Aanwezigheidslijst opstellen\n"
              "b: Personen op foto omcirkelen\n"
              "c: Beide opties")
        antw = input("a, b, c: ")
        if antw == 'a' or antw == 'b' or antw == 'c':
            inp_afb = input("Geef het pad naar de afbeelding met de aanwezigen: ")
        else:
            raise ValueError
        if antw == 'a' or antw == 'c':
            outp_csv = input("Waar wilt u de ledenlijst opslaan?: ")
            if antw == 'a':
                self.oplijster.get_list(inp_afb, outp_csv, datetime.date.today())
        if antw == 'b' or antw == 'c':
            outp_abf = input("Waar wilt uw de aangepaste afbeelding opslaan?: ")
            if antw == 'b':
                self.oplijster.draw_rect(inp_afb, outp_abf, datetime.date.today())
        if antw == 'c':
            self.oplijster.get_list_draw_rect(inp_afb, outp_abf, outp_csv, datetime.date.today())

    def volledig_proces(self):
        print("--VOLLEDIGE LEDENLIJST PROCES---")
        self.uitknippen()
        self.trainen()
        self.oplijsten()


if __name__ == "__main__":
    oProgramma = Programma()
    # oProgramma.volledig_proces()
    oProgramma.trainen()
    oProgramma.oplijsten()
