import os
import argparse
from flask import Flask, request, jsonify
from intent_classifier import IntentClassifier
from logging_config import setup_logging
from flasgger import Swagger, swag_from

# Initialize logger
logger = setup_logging()

def create_app(model_path=None):
    app = Flask(__name__)
    swagger = Swagger(app)
    
    model = IntentClassifier()
    if model_path:
        model.load(model_path)  # Load the model during app creation
    
    @app.route('/ready')
    @swag_from({
        'responses': {
            '200': {
                'description': 'Service is ready',
            },
            '423': {
                'description': 'Service is not ready',
            }
        }
    })
    def ready():
        if model.is_ready():
            return 'OK', 200
        else:
            return 'Not ready', 423

    @app.route('/intent', methods=['POST'])
    @swag_from({
        'tags': ['Intent Classification'],
        'summary': 'Classify the intent of the given text',
        'description': 'Receives a JSON payload with a text field and returns the intent classification result.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'text': {
                            'type': 'string',
                            'description': 'Text to classify'
                        }
                    },
                    'required': ['text']
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Successful response with intent classification',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'label': {
                            'type': 'string',
                            'description': 'Intent label'
                        },
                        'message': {
                            'type': 'string',
                            'description': 'Additional message'
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad request when text is empty or invalid'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    })
    def intent():
        try:
            data = request.json
            text = data.get('text', '')
            logger.info(f'Received request data: {data}')

            if not text:
                return jsonify({"label": "TEXT_EMPTY", "message": "\"text\" is empty."}), 400

            response, status_code = model.predict(text)
            logger.info(f'Prediction result: {response}')
            return jsonify(response), status_code
        except Exception as e:
            logger.error(f'Error during prediction: {e}', exc_info=True)
            return jsonify({"label": "INTERNAL_ERROR", "message": str(e)}), 500

    return app

def main():
    model_path_default = os.path.join(os.getcwd(), 'models', 'intent_classification1.keras')
    port_default = os.getenv('PORT', 8080)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--model', type=str, default=model_path_default, help='Path to model directory or file.')
    arg_parser.add_argument('--port', type=int, default=port_default, help='Server port number.')
    args = arg_parser.parse_args()

    app = create_app(args.model)
    app.run(host="0.0.0.0", port=args.port)

if __name__ == '__main__':
    #http://localhost:8080/apidocs/
    #http://localhost:8080/intent
    main()
