from cgitb import text
import unittest

from fastapi.testclient import TestClient

from geocalc.api.main import app

class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_client = TestClient(app)

    def get_iou(self, params=None):
        return self.api_client.get('/calculations/iou', params=params)

    def test_root_endpoint_success(self):
        response = self.api_client.get('/')
        assert response.status_code == 200

    def test_iou_endpoint_query_params_validation(self):
        # no query params at all
        response = self.get_iou()
        self.assertEqual(response.status_code, 422)

        # one box missing
        response = self.get_iou({
            'box1': (0, 2, 2, 0)
        })
        self.assertEqual(response.status_code, 422)

        # some coordinatess missing
        response = self.get_iou({
            'box1': [0, 2.12, 2],
            'box2': [0, 1, 1.8, 0]
        })
        self.assertEqual(response.status_code, 422)
        self.assertTrue('box1 should contain 4 float values in order:' in response.text)
        
        # incorrect type of some of the coordinates
        response = self.get_iou({
            'box1': ['', 2, 2, 'a'],
            'box2': [0, 1, 1, 0]
        })
        self.assertEqual(response.status_code, 422)

        # top-left and bottom-right corners of box2 are misaligned
        response = self.get_iou({
            'box1': [0, 2, 2, 0],
            'box2': [2, 0, 0, 2]
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            '{"detail":"box2 bottom right point {x: 0.0, y: 2.0} should be to the right of top left {x: 2.0, y: 0.0}"}',
            response.text
        )

    def test_iou_endpoint_success(self):
        response = self.get_iou({
            'box1': (0, 10, 10, 0),
            'box2': (5, 10, 15, 0)
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"result":0.333}')
