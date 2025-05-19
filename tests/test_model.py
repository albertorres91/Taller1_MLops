import unittest
from model.app.model import clasificar_estado_salud_sin_presion

class TestModeloEnfermedad(unittest.TestCase):
    def test_prediccion_enfermedad_leve(self):
        """Prueba que el modelo devuelve ENFERMEDAD LEVE con síntomas leves"""
        resultado = clasificar_estado_salud_sin_presion(
            sintomas=["leve dolor de cabeza"],
            temperatura=36.5,
            edad=25,
            sexo="maculino",
            frecuencia_cardiaca=70
        )
        self.assertEqual(resultado, "ENFERMEDAD LEVE")
    
    def test_prediccion_enfermedad_grave(self):
        """Prueba que el modelo devuelve ENFERMEDAD GRAVE con síntomas graves"""
        resultado = clasificar_estado_salud_sin_presion(
            sintomas=["fiebre alta", "dificultad para respirar"],
            temperatura=39.5,
            edad=65,
            sexo="femenino",
            frecuencia_cardiaca=110
        )
        self.assertEqual(resultado, "ENFERMEDAD GRAVE")