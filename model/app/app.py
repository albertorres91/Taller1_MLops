from fastapi import FastAPI, HTTPException
import uvicorn
import logging
import os
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

app = FastAPI(
    title="API de ayuda al Diagnóstico Médico",
    description="Ayuda médica para diagnóstico a partir de síntomas y evluación clínica objetiva",
    version="1.0.1"
)

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

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)