import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np


class Predict():
    def __init__(self) -> None:
        self.model_name = "model.h5"
        self.model = self.load_model(self.model_name)
        self.labels = pd.read_csv("labels.csv")
        self.unique_breeds = np.unique(self.labels.breed)
        self.formatted_breeds = [name.title() for name in self.unique_breeds]
        self.IMAGE_SIZE = 224
        self.BATCH_SIZE = 32

    def image_to_tensor(self, imagepath):
        # Read file
        image = tf.io.read_file(imagepath)
        # Convert file in a numerical tensor
        image = tf.image.decode_jpeg(image, channels=3)
        # Convert values between 0-255 to 0-1
        image = tf.image.convert_image_dtype(image, tf.float32)
        # Resize the image
        image = tf.image.resize(image, size=[self.IMAGE_SIZE, self.IMAGE_SIZE])

        return image

    def get_image_label(self, path_image, label):
        image = self.image_to_tensor(imagepath=path_image)
        return image, label

    def create_data_batches(self, X, y=None, valid_data=False, test_data=False):
        if test_data:
            print("Creating test data batches...")
            data = tf.data.Dataset.from_tensor_slices(
                ([X]))  # Wrap X in a list

            data_batch = data.map(self.image_to_tensor).batch(self.BATCH_SIZE)
            return data_batch

        elif valid_data:
            print("Creating validation data batches...")
            data = tf.data.Dataset.from_tensor_slices(
                (tf.constant(X), tf.constant(y)))

            data_batch = data.map(self.get_image_label).batch(self.BATCH_SIZE)
            return data_batch

        else:
            print("Creating training data batches...")
            data = tf.data.Dataset.from_tensor_slices(
                (tf.constant(X), tf.constant(y)))
            # Shuffle
            data = data.shuffle(buffer_size=len(X))

            data = data.map(self.get_image_label)

            data_batch = data.batch(self.BATCH_SIZE)
            return data_batch

    def load_model(self, model_path):
        print(f"Loading a model from {model_path}")
        model = tf.keras.models.load_model(model_path, custom_objects={
                                           "KerasLayer": hub.KerasLayer})
        return model

    def breed(self, predicted):
        for breed in self.formatted_breeds:
            if str(predicted).lower() == str(breed).lower():
                return (breed.replace('_', ' '))

    def predict_image(self, imagepath):
        image_batch = self.create_data_batches(imagepath, test_data=True)

        prediction = self.model.predict(image_batch, verbose=True)

        index = 0
        percentage = (np.max(prediction[index])) * 100
        predicted_breed = self.breed(
            self.unique_breeds[np.argmax(prediction[index])])

        return {"percentage": round(percentage, 2), "predicted_breed": predicted_breed}
