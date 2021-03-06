import os
import pickle
import face_recognition as fr


class Trainen():
    FILE_TYPES = ('.jpg', '.JPG', '.jpeg', '.JPEG')

    def __init__(self, report=None):
        self.report = report
        self.known_names = []
        self.known_name_encodings = []

    def train(self, inp_path: str):
        """
        Zal de mappen in inp_path scannen op afbeeldingen met gezichten en
        daar de encodings van opslaan in een lijst.
        :param inp_path: str Pad naar mappen die genoemd zijn naar de persoon waarvan het gezicht in de map zit.
        """
        # Training directory
        if inp_path[-1] != '/':
            inp_path += '/'
        train_dir = os.listdir(inp_path)

        # Loop through each person in the training directory
        for person in train_dir:
            if os.path.isdir(inp_path + person):
                pix = os.listdir(inp_path + person)

                # Loop through each training image for the current person
                for person_img in pix:
                    if person_img.endswith(Trainen.FILE_TYPES):
                        # Get the face encodings for the face in each image file
                        face = fr.load_image_file(
                            inp_path + person + "/" + person_img)
                        face_bounding_boxes = fr.face_locations(face)

                        # If training image contains exactly one face
                        if len(face_bounding_boxes) == 1:
                            face_enc = fr.face_encodings(face)[0]
                            # Add face encoding for current image
                            # with corresponding label (name) to the training data
                            self.known_names.append(person)
                            self.known_name_encodings.append(face_enc)
                            outputting = person + "/" + person_img + " toegevoegd!"
                            print(outputting)
                            if self.report is not None:
                                self.report.print(outputting)

                        else:
                            outputting = person + "/" + person_img + " can't be used for training"
                            print(outputting)
                            if self.report is not None:
                                self.report.print(outputting)

    def export_faces(self, outp_path: str):
        """
        Exporteer de namen en gezichtsencodings naar een bestand.
        :param outp_path: Plaats om het pickle bestand op te slaan.
        """
        export_data = {
            "known_names": self.known_names,
            "known_name_encodings": self.known_name_encodings
        }
        with open(outp_path + "face_encodings.pickle", "wb") as fh:
            pickle.dump(export_data, fh)

        outputting = "Export opgeslagen in: " + outp_path + "face_encodings.pickle"
        print(outputting)
        if self.report is not None:
            self.report.print(outputting)

    def import_faces(self, pickle_path: str):
        """
        Importeert namen en gezichtsencodings in de klasse om later te gebruiken.
        Dit bespaart veel rekenkracht in vergelijking met iedere keer opnieuw de encodings te berekenen.
        :param pickle_path: Pad naar het .pickle bestand.
        """
        with open(pickle_path, "rb") as fh:
            import_data = pickle.load(fh)

        self.known_names = import_data["known_names"]
        self.known_name_encodings = import_data["known_name_encodings"]
        outputting = f"{pickle_path} ge??mporteerd."
        print(outputting)
        if self.report is not None:
            self.report.print(outputting)


if __name__ == "__main__":
    oTraining = Trainen()
    oTraining.train("./Trainen/gezichten/")
    oTraining.export_faces("./Trainen/")

    oTraining2 = Trainen()
    oTraining2.import_faces("./Trainen/face_encodings.pickle")
