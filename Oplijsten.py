import csv
import datetime

import face_recognition as fr
import cv2
import numpy as np

from Trainen import Trainen


class Oplijsten():
    def __init__(self, training: Trainen, report=None):
        self.report = report
        self.training = training

    def _find_matches(self, inp_afb: str, datum: datetime.date, draw_rect=False, get_list=False):
        """
        Vind gezichten in de aangegeven afbeelding en vergelijkt ze met de encodings in de Trainen instantie.
        Kan een kader teken rond de gevonden personen of een lijst samenstellen.
        De datum komt in de hoek van de afbeelding en bovenaan de aanwezigheidslijst.
        :param inp_afb: Afbeelding met mensen die we willen herkennen.
        :param datum: Datum van de vergadering.
        :param draw_rect: False of het pad naar de locatie voor het uitgangsbestand.
        :param get_list: False of het pad naar de locatie voor de aanwezigheidslijst.
        """
        image = cv2.imread(inp_afb)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)

        if get_list:
            with open(get_list, mode='w') as leden_file:
                ledenlijst = csv.writer(leden_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                ledenlijst.writerow([str(datum)])

        if draw_rect:
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, str(datum), (10, 50), font, 1.0, (255, 255, 255), 1)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(self.training.known_name_encodings, face_encoding)
            name = ""

            face_distances = fr.face_distance(self.training.known_name_encodings, face_encoding)
            best_match = np.argmin(face_distances)

            if matches[best_match]:
                name = self.training.known_names[best_match]
                outputting = f"{name} gevonden in {inp_afb}"
                print(outputting)
                if self.report is not None:
                    self.report.print(outputting)
                if get_list:
                    with open(get_list, mode='a+') as leden_file:
                        ledenlijst = csv.writer(leden_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        ledenlijst.writerow([name])

            if draw_rect:
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                cv2.imwrite(draw_rect, image)

    def draw_rect(self, inp_afb, outp_afb, datum: datetime.date):
        """ Gebruikt _find_matches()
        Goed om een test uit te voeren.
        Zal een afbeelding maken waar alle herkende gezichten omcirkeld zijn met naam erbij.
        :param inp_afb: Afbeelding met mensen die we willen herkennen.
        :param outp_afb: Pad naar inp_afb met herkende gezichten omcirkeld en naam toegevoegd.
        :param datum: Datum van de vergadering.
        """
        self._find_matches(inp_afb, datum, draw_rect=outp_afb)

    def get_list(self, inp_afb, outp_file, datum: datetime.date):
        """ Gebruikt _find_matches()
        Laat je een aanwezigheidslijst genereren in CSV formaat.
        :param inp_afb: Afbeelding met mensen die we willen herkennen.
        :param outp_file: Pad naar de locatie voor de aanwezigheidslijst.
        :param datum: Datum van de vergadering.
        """
        self._find_matches(inp_afb, datum, get_list=outp_file)

    def get_list_draw_rect(self, inp_afb, outp_afb, outp_file, datum: datetime.date):
        """ Gebruikt _find_matches()
        Zal een afbeelding maken waar alle herkende gezichten omcirkeld zijn met naam erbij
        en zal een aanwezigheidslijst genereren in CSV formaat.
        :param inp_afb: Afbeelding met mensen die we willen herkennen.
        :param outp_afb: Pad naar inp_afb met herkende gezichten omcirkeld en naam toegevoegd.
        :param outp_file: Pad naar de locatie voor de aanwezigheidslijst.
        :param datum: Datum van de vergadering.
        """
        self._find_matches(inp_afb, datum, draw_rect=outp_afb, get_list=outp_file)


if __name__ == "__main__":
    oTraining = Trainen()
    oTraining.import_faces("./Trainen/face_encodings.pickle")

    oOplijsting = Oplijsten(oTraining)
    oOplijsting.get_list_draw_rect("./Trainen/test1.jpg", "./Trainen/_test1.jpg", "./Trainen/_test1.csv",
                                   datetime.date.today())
    oOplijsting.get_list("./Trainen/test2.jpeg", "./Trainen/_test2.csv", datetime.date(2002, 9, 30))
    oOplijsting.draw_rect("./Trainen/test3.jpg", "./Trainen/_test3.jpg", datetime.date(2002, 9, 30))
