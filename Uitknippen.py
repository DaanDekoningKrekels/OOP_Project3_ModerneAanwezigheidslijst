import os

import dlib
from PIL import Image
from matplotlib import pyplot as plt


class Uitknippen():
    FILE_TYPES = ('.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG')

    def __init__(self, dest_path: str, max_dimension: int = 200, simple_crop: bool = True):
        self.dest_path = dest_path
        self.max_dimension = max_dimension
        self.simple_crop = simple_crop
        self.face_detector = dlib.get_frontal_face_detector()
        self.files = []
        self.filenames = []

    def findFiles(self, source_path: str, ) -> bool:
        try:
            for file_i in os.listdir(source_path):
                if file_i.endswith(Uitknippen.FILE_TYPES):
                    self.files.append(file_i)

            for fname in self.files:
                self.filenames.append(os.path.join(source_path, fname))

            print('found %d files' % len(self.filenames))
            return True
        except:
            return False

    def cropFaces(self):
        filename_inc = 100

        filecount = 1

        for file in self.filenames:
            img = plt.imread(file)
            detected_faces = self.face_detector(img, 1)
            print("[%d of %d] %d detected faces in %s" % (filecount, len(self.filenames), len(detected_faces), file))
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
                    cropped_image.save(self.dest_path + "/" + str(filename_inc) + ".jpg", "JPEG")
                    filename_inc += 1
            filecount += 1


if __name__ == "__main__":
    oUitknippen = Uitknippen("./Uitknippen/cropped/")
    oUitknippen.findFiles("./Uitknippen/source/")
    oUitknippen.cropFaces()
