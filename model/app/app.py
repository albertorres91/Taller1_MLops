from model.app.model import diagnosis
import pandas as pd 
from fastapi import FastAPI
import uvicorn
import logging
import os

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
logger.log(logging.INFO, "Iniciando la aplicación FastAPI")

app = FastAPI()

@app.get('/')
async def root():  
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": "Bienvenido a la API de predicción de diagnóstico "+__name__+"."}


@app.post('/predictions')
async def procesar_diagnostico():
    """
    Endpoint para recibir datos y devolver una predicción.
    """
    logger.info("Recibiendo datos para predicción")
    try :
        prediction = diagnosis()
        print("Predicción en appp.py:", prediction)  
    except Exception as e:
        #logger.error(f"Error en la predicción: {e}")
        print(f"Error en la predicción: {e}")    
        return {"error": "Error en la predicción"}
    return {'diagnostico': prediction[0]}

if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=5000, reload=True)
