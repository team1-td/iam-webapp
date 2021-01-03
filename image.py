import imghdr
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


model = ResNet50(weights='imagenet')

class Image:

    def __init__(self, image_path):
        self.image_path = image_path
        self.classification = ''

    def is_image_format_valid(self):
        if imghdr.what(self.image_path) in ['png', 'jpg', 'jpeg']:
            return True
        return False

    def classify_image(self):
        img = image.load_img(self.image_path, target_size=(224, 224))
        image_array = image.img_to_array(img)
        image_array = np.expand_dims(image_array, axis=0)
        image_array = preprocess_input(image_array)

        preds = model.predict(image_array)
        # decode the results into a list of tuples (class, description, probability)
        predictions = decode_predictions(preds, top=3)

        if predictions[0][0][2] >= 0.4:  # set probability more than 0.4
            self.classification = predictions[0][0][1]
        else:
            self.classification = 'unknown'
