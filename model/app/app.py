from fastapi import FastAPI, HTTPException
import uvicorn
import logging
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from .model import clasificar_estado_salud_sin_presion, diag  # Importación relativa

# Crear un modelo Pydantic para validar la entrada
from pydantic import BaseModel, Field
from typing import List, Optional

class PacienteInput(BaseModel):
    sintomas: List[str] = Field(default=[])
    temperatura: float = Field(...)
    edad: int = Field(...)
    sexo: str = Field(...)
    frecuencia_cardiaca: int = Field(...)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Iniciando la aplicación FastAPI detección de enfermedades huérfanas y comunes")

# Configuración de archivos
PREDICTIONS_FILE = "predictions_log.json"
STATS_FILE = "predictions_stats.json"

# Crear archivos si no existen
Path(PREDICTIONS_FILE).touch(exist_ok=True)
Path(STATS_FILE).touch(exist_ok=True)

app = FastAPI(
    title="API de ayuda al Diagnóstico Médico",
    description="Ayuda médica para diagnóstico a partir de síntomas y evaluación clínica objetiva",
    version="1.0.1"
)

def save_prediction_to_file(prediction_data: Dict):
    """Guarda la predicción en el archivo de registros"""
    try:
        # Leer predicciones existentes
        existing_data = []
        if os.path.getsize(PREDICTIONS_FILE) > 0:
            with open(PREDICTIONS_FILE, 'r') as f:
                existing_data = json.load(f)
        
        # Agregar nueva predicción
        existing_data.append(prediction_data)
        
        # Mantener solo las últimas 1000 predicciones para evitar archivos muy grandes
        if len(existing_data) > 1000:
            existing_data = existing_data[-1000:]
        
        # Guardar
        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        # Actualizar estadísticas
        update_stats(prediction_data['diagnostico'])
        
    except Exception as e:
        logger.error(f"Error guardando predicción: {str(e)}")

def update_stats(diagnostico: str):
    """Actualiza las estadísticas de predicciones"""
    try:
        # Leer estadísticas existentes
        stats = {}
        if os.path.getsize(STATS_FILE) > 0:
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        
        # Inicializar categoría si no existe
        if 'categorias' not in stats:
            stats['categorias'] = {
                'NO ENFERMO': 0,
                'ENFERMEDAD LEVE': 0,
                'ENFERMEDAD AGUDA': 0,
                'ENFERMEDAD CRÓNICA': 0,
                'ENFERMEDAD TERMINAL': 0
            }
        
        # Actualizar contador de categoría
        stats['categorias'][diagnostico] += 1
        
        # Actualizar última predicción
        stats['ultima_prediccion'] = datetime.now().isoformat()
        
        # Guardar
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error actualizando estadísticas: {str(e)}")

def get_stats_report() -> Dict:
    """Genera el reporte estadístico"""
    try:
        # Leer estadísticas
        stats = {}
        if os.path.getsize(STATS_FILE) > 0:
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        
        # Leer últimas predicciones
        predictions = []
        if os.path.getsize(PREDICTIONS_FILE) > 0:
            with open(PREDICTIONS_FILE, 'r') as f:
                predictions = json.load(f)
        
        # Formatear reporte
        report = {
            'total_por_categoria': stats.get('categorias', {}),
            'ultima_prediccion': stats.get('ultima_prediccion'),
            'ultimas_5_predicciones': predictions[-5:][::-1]  # Más reciente primero
        }
        
        return report
        
    except Exception as e:
        logger.error(f"Error generando reporte: {str(e)}")
        return {
            'error': 'No se pudo generar el reporte',
            'detalle': str(e)
        }

@app.get('/')
async def root():
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": "Bienvenido a la API de predicción de diagnóstico médico"}

@app.post('/predictions')
async def procesar_diagnostico(paciente: PacienteInput):
    """
    Endpoint para recibir datos del paciente y devolver una predicción de diagnóstico.
    """
    logger.info(f"Recibiendo datos para predicción: {paciente}")
    try:
        # Usar el modelo completo de clasificación
        resultado = clasificar_estado_salud_sin_presion(
            sintomas=paciente.sintomas,
            temperatura=paciente.temperatura,
            edad=paciente.edad,
            sexo=paciente.sexo,
            frecuencia_cardiaca=paciente.frecuencia_cardiaca
        )
        
        # Verificar si hay error en la validación
        if isinstance(resultado, str) and resultado.startswith("Error:"):
            raise HTTPException(status_code=400, detail=resultado)
            
        logger.info(f"Diagnóstico generado: {resultado}")
        
        # Guardar la predicción
        prediction_data = {
            'fecha': datetime.now().isoformat(),
            'diagnostico': resultado,
            'datos_paciente': {
                'sintomas': paciente.sintomas,
                'temperatura': paciente.temperatura,
                'edad': paciente.edad,
                'sexo': paciente.sexo,
                'frecuencia_cardiaca': paciente.frecuencia_cardiaca
            }
        }
        
        save_prediction_to_file(prediction_data)
        
        return {'diagnostico': resultado}
    except Exception as e:
        logger.error(f"Error en la predicción: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")

@app.get('/random')
async def random_diagnostico():
    """
    Endpoint para obtener un diagnóstico aleatorio (para pruebas).
    """
    prediction = diag()
    return {'diagnostico': prediction[0]}

@app.get('/reporte_estadisticas', response_model=Dict)
async def obtener_reporte_estadisticas():
    """
    Endpoint para obtener el reporte estadístico de las predicciones realizadas.
    Devuelve:
    - Número total de predicciones por categoría
    - Últimas 5 predicciones realizadas
    - Fecha de la última predicción
    """
    try:
        reporte = get_stats_report()
        return reporte
    except Exception as e:
        logger.error(f"Error generando reporte estadístico: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generando reporte estadístico")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)