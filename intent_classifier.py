# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import keras
import re, string
from logging_config import setup_logging
logger = setup_logging()

class IntentClassifier:
    def __init__(self):
        self.model = None
        self.max_len = 50
        self.original_labels = np.array(['aircraft', 'airfare_info', 'airline_info', 'flight_info',
       'ground_service_info', 'location_info', 'misc_info'], dtype=object)

    @keras.utils.register_keras_serializable()
    def custom_standardization(input_data):
        try:
            # 1. Convert to lowercase
            lowercase = tf.strings.lower(input_data)
            
            # 2. Remove punctuation
            stripped_punctuation = tf.strings.regex_replace(lowercase, f"[{re.escape(string.punctuation)}]", "")
            
            # 3. Remove extra whitespace
            return tf.strings.strip(stripped_punctuation)
        except Exception as e:
            logger.error(f'Error during standardization: {e}', exc_info=True)

    def load(self, model_path):
        # Load the trained model
        logger.info(f'Model Path: {model_path}')
        self.model = load_model(model_path)
        if self.model is None:
            logger.info("Model Not loaded")
        else:
            logger.info("Model loaded")

    def is_ready(self):
        return self.model is not None

    def predict(self, text):
        try:
            text_input = tf.convert_to_tensor([text], dtype=tf.string) 

            # Step 1: Predict using the trained model
            probabilities = self.model.predict(text_input)[0]  # Get probability distribution
            
            # Step 2: Get the top 3 predicted class indices
            top_3_indices = np.argsort(probabilities)[-3:][::-1]
            
            # Step 3: Map indices back to original labels
            top_3_labels = self.original_labels[top_3_indices]
            
            # Step 4: Prepare the JSON response
            predictions = [
                {"label": label, "confidence": round(float(probabilities[index]),2)}
                for label, index in zip(top_3_labels, top_3_indices)
            ]
            
            return {"intents": predictions}, 200
        except Exception as e:
            logger.error(f'Error during prediction: {e}', exc_info=True)
            return {"label": "INTERNAL_ERROR", "message": str(e)}, 500

if __name__ == '__main__':
    pass
