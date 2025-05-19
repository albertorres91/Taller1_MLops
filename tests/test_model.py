import unittest
from model.app.model import clasificar_estado_salud_sin_presion  # Ajusta según tu implementación real

class TestModeloEnfermedad(unittest.TestCase):
    def setUp(self):
        self.modelo = clasificar_estado_salud_sin_presion()
        # Opcional: Resetear estadísticas antes de cada prueba
    
    def test_prediccion_enfermedad_leve(self):
        """Prueba que el modelo devuelve ENFERMEDAD LEVE con síntomas leves"""
        resultado = self.modelo.predecir(edad=20, sintomas=["respiratorios leves"], condiciones=["neurológica leve"])
        self.assertEqual(resultado, "ENFERMEDAD LEVE")
    
    def test_prediccion_enfermedad_grave(self):
        """Prueba que el modelo devuelve ENFERMEDAD GRAVE con síntomas graves"""
        resultado = self.modelo.predecir(edad=75, sintomas=["respiratorios graves", "fiebre alta"], condiciones=[])
        self.assertEqual(resultado, "ENFERMEDAD GRAVE")
    
    def test_estadisticas_iniciales_vacias(self):
        """Prueba que las estadísticas iniciales están vacías o con valores por defecto"""
        stats = self.modelo.obtener_estadisticas()
        self.assertTrue(
            stats == {} or 
            all(v == 0 for v in stats.values())  # Depende de tu implementación
        )
    
    def test_actualizacion_estadisticas(self):
        """Prueba que las estadísticas se actualizan correctamente después de una predicción"""
        # Primero verificamos que está vacío
        stats_inicial = self.modelo.obtener_estadisticas()
        
        # Realizamos una predicción
        self.modelo.predecir(edad=30, sintomas=["dolor de cabeza"], condiciones=[])
        
        # Verificamos que las estadísticas cambiaron
        stats_final = self.modelo.obtener_estadisticas()
        self.assertNotEqual(stats_inicial, stats_final)
    
    def test_cobertura_categorias(self):
        """Prueba que el modelo puede devolver todas las categorías de enfermedades"""
        casos_prueba = [
            ({"edad": 20, "sintomas": ["leves"], "condiciones": []}, "ENFERMEDAD LEVE"),
            ({"edad": 40, "sintomas": ["moderados"], "condiciones": []}, "ENFERMEDAD MODERADA"),
            ({"edad": 60, "sintomas": ["graves"], "condiciones": []}, "ENFERMEDAD GRAVE"),
            ({"edad": 25, "sintomas": [], "condiciones": ["crónica"]}, "CONDICIÓN CRÓNICA"),
            ({"edad": 70, "sintomas": ["graves"], "condiciones": ["crónica"]}, "URGENCIA MÉDICA")
        ]
        
        for entrada, esperado in casos_prueba:
            resultado = self.modelo.predecir(**entrada)
            self.assertEqual(resultado, esperado)