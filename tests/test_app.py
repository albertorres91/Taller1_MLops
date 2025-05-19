import unittest
from model.app.app import app  # Ajusta según tu implementación real
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_endpoint_prediccion(self):
        """Prueba el endpoint de predicción"""
        respuesta = self.app.post('/predecir', json={
            "edad": 30,
            "sintomas": ["dolor de cabeza"],
            "condiciones": []
        })
        self.assertEqual(respuesta.status_code, 200)
        datos = json.loads(respuesta.data)
        self.assertIn("resultado", datos)
    
    def test_endpoint_estadisticas(self):
        """Prueba el endpoint de estadísticas"""
        respuesta = self.app.get('/estadisticas')
        self.assertEqual(respuesta.status_code, 200)
        datos = json.loads(respuesta.data)
        self.assertIsInstance(datos, dict)