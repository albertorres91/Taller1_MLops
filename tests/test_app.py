import unittest
from fastapi.testclient import TestClient  # Cambio importante aquí
from model.app.app import app  # Asegúrate que esta ruta es correcta

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)  # Así se usa en FastAPI
    
    def test_endpoint_prediccion(self):
        """Prueba el endpoint de predicción"""
        respuesta = self.client.post('/predictions', json={
            "edad": 30,
            "sintomas": ["dolor de cabeza"],
            "condiciones": []
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("resultado", respuesta.json())
    
    def test_endpoint_estadisticas(self):
        """Prueba el endpoint de estadísticas"""
        respuesta = self.client.get('/reporte_estadisticas')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsInstance(respuesta.json(), dict)