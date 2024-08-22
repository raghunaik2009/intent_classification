import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import create_app

class TestIntentClassifier(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Provide the correct path to your model here
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'intent_classification1.keras')
        cls.app = create_app(model_path).test_client()
        cls.app.testing = True

    def test_ready(self):
        response = self.app.get('/ready')
        self.assertEqual(response.status_code, 200)

    def test_intent(self):
        response = self.app.post('/intent', json={'text': 'find me a flight'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('intents', response.json)

    def test_empty_text(self):
        response = self.app.post('/intent', json={'text': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('TEXT_EMPTY', response.json['label'])

if __name__ == '__main__':
    unittest.main()
