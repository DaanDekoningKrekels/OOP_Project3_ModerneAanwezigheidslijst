import os

import dlib
from PIL import Image
from matplotlib import pyplot as plt


class Uitknippen():
    FILE_TYPES = ('.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG')

    def __init__(self, max_dimension: int = 200, simple_crop: bool = True, report=None):
        """
        Klasse die helpt gezichten uit te knippen van afbeeldingen.
        :param max_dimension: Maximum afmetingen voor uitgesneden gezichten.
        :param simple_crop: Try it.
        """
        self.max_dimension = max_dimension
        self.simple_crop = simple_crop
        self.report = report
        self.face_detector = dlib.get_frontal_face_detector()
        self.files = []
        self.filenames = []

    def findFiles(self, source_path: str, ) -> bool:
        """
        Vind de ondersteunde afbeelding bestanden in een meegegeven map.
        :param source_path: str Map waarin naar afbeeldingen wordt gezocht.
        :return: bool: True als er niets misging
        """
        try:
            for file_i in os.listdir(source_path):
                if file_i.endswith(Uitknippen.FILE_TYPES):
                    self.files.append(file_i)

            for fname in self.files:
                self.filenames.append(os.path.join(source_path, fname))
            outputting = '%d bestanden gevonden.' % len(self.filenames)
            print(outputting)
            if self.report is not None:
                self.report.print(outputting)
            return True
        except:
            return False

    def cropFaces(self, dest_path: str):
        """ https://gist.github.com/mcclux/afb41e8217c83fb15173f76effaf2345
        Knip de gevonden gezichten uit naar een bepaalde map.
        :param dest_path: Map om alle gevonden gezichten in te plaatsen.
        """
        filename_inc = 100
        filecount = 1

        for file in self.filenames:
            img = plt.imread(file)
            detected_faces = self.face_detector(img, 1)
            outputting = "[%d of %d] %d detected faces in %s" % (
                filecount, len(self.filenames), len(detected_faces), os.path.basename(file))
            print(outputting)
            if self.report is not None:
                self.report.print(outputting)
            for i, face_rect in enumerate(detected_faces):
                width = face_rect.right() - face_rect.left()
                height = face_rect.bottom() - face_rect.top()
                if width >= self.max_dimension and height >= self.max_dimension or True:
                    image_to_crop = Image.open(file)

                    if self.simple_crop:
                        crop_area = (face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom())
                    else:
                        size_array = []
                        size_array.append(face_rect.top())
                        size_array.append(image_to_crop.height - face_rect.bottom())
                        size_array.append(face_rect.left())
                        size_array.append(image_to_crop.width - face_rect.right())
                        size_array.sort()
                        short_side = size_array[0]
                        crop_area = (
                            face_rect.left() - size_array[0], face_rect.top() - size_array[0],
                            face_rect.right() + size_array[0],
                            face_rect.bottom() + size_array[0])

                    cropped_image = image_to_crop.crop(crop_area)
                    crop_size = (self.max_dimension, self.max_dimension)
                    cropped_image.thumbnail(crop_size)
                    cropped_image.save(dest_path + "/" + str(filename_inc) + ".jpg", "JPEG")
                    filename_inc += 1
            filecount += 1


if __name__ == "__main__":
    oUitknippen = Uitknippen()
    oUitknippen.findFiles("./Uitknippen/source/")
    oUitknippen.cropFaces("./Uitknippen/cropped/")
