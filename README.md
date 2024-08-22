# Intent Classification Service

## Overview

This repository contains a service for intent classification using a neural network model. The service is designed to classify user intents based on text input and is implemented using Flask. The model is trained using the ATIS dataset. This README provides instructions on setting up, running, and testing the service.

## Project Structure

- `server.py`: Contains the Flask application with endpoints for service readiness and intent classification.
- `intent_classifier.py`: Defines the `IntentClassifier` class for loading the model and performing predictions.
- `test_server.py`: Contains unit tests for the Flask application.
- `Dockerfile`: Docker configuration to containerize the application.
- `requirements.txt`: Python dependencies required for the application.
- `model_training_notebook.ipynb`: Jupyter Notebook with details on model training, preprocessing steps, and evaluation.

## Model Overview

### Dataset

The model is trained using the **ATIS** dataset, which is widely used for intent classification tasks in natural language processing (NLP). The dataset consists of sentences related to flight information, each labeled with a specific intent.

### Model Architecture

The intent classification model is implemented using TensorFlow and Keras. The model architecture includes:

- **TextVectorization Layer**: To preprocess and standardize the input text.
- **Embedding Layer**: To convert text into dense vectors of fixed size.
- **LSTM Layer**: To capture sequential dependencies in the text.
- **Dense Layers**: To classify the processed text into one of the predefined intent categories.

### Training and Evaluation

The model was trained on the ATIS dataset, achieving the following results:

- **Accuracy**: 96% on the test data
- **F1 Score**: Close to 90%

The model was evaluated using multiple metrics:

- **Accuracy**: Measures the overall correctness of the model.
- **F1 Score**: Balances precision and recall, providing a single metric for model performance.
- **Recall**: Measures the model's ability to correctly identify positive instances.
- **Precision**: Measures the model's accuracy in predicting positive instances.

The complete training and evaluation process is documented in the provided Jupyter notebook (`notebook/model_training.ipynb`).

## API Documentation

### Accessing the service
- **URL**: `http://localhost:8080/apidocs/`
- **URL**: `http://localhost:8080/intent`

### `GET /ready`

- **Description**: Checks if the service is running and the model is loaded.
- **Responses**:
  - `200 OK`: Service is ready.
  - `423 Not Ready`: Model has not been loaded.

### `POST /intent`

- **Description**: Classifies the intent of the provided text.
- **Request**:
  - **Content-Type**: `application/json`
  - **Body**:
    ```json
    {
      "text": "find me a flight that flies from Memphis to tacoma"
    }
    ```
- **Response**:
  - **200 OK**:
    ```json
    {
      "intents": [
        {"label": "flight", "confidence": 0.73},
        {"label": "aircraft", "confidence": 0.12},
        {"label": "capacity", "confidence": 0.03}
      ]
    }
    ```
  - **400 Bad Request**: If the text is empty.
    ```json
    {
      "label": "TEXT_EMPTY",
      "message": "\"text\" is empty."
    }
    ```
  - **500 Internal Server Error**: For any internal errors.
    ```json
    {
      "label": "INTERNAL_ERROR",
      "message": "<ERROR_MESSAGE>"
    }
    ```

## Setup and Installation

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerization)

### Installing Dependencies

1. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Training the Model

Detailed information on model training, preprocessing steps, and evaluation can be found in the [intent_classification.ipynb](intent_classification.ipynb). This notebook provides a comprehensive overview of:

- **Data Preprocessing**: Cleaning and preparing the ATIS dataset for model training.
- **Model Training**: Building and training the neural network model.
- **Evaluation**: Assessing model performance and making improvements.

Please ensure you have a trained model saved as `intent_classification1.keras` in the `models` directory before running the service.

## Running the Service

### Using Flask

To run the service locally:

1. Ensure the model file is available at `models/intent_classification1.keras`.

2. Run the Flask application:
    ```bash
    python server.py --model models/intent_classification1.keras --port 8080
    ```

### Using Docker

To build and run the Docker container:

1. Build the Docker image:
    ```bash
    docker build -t intent-classifier:v1 .
    ```

2. Run the Docker container:
    ```bash
    docker run -p 8080:8080 intent-classifier:v1
    ```

## Testing

### Unit Tests

To run the unit tests:

1. Ensure the model file is available at `models/intent_classification1.keras`.

2. Run the tests:
    ```bash
    pytest tests/test_server.py
    ```
