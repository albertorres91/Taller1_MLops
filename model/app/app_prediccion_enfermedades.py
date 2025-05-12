import streamlit as st
import pandas as pd
import numpy as np

# Simulación de modelo real con reglas básicas de decisión

def modelo_simulado(data):
    temperatura = data['temperatura']
    presion_sistolica = data['presion_sistolica']
    presion_diastolica = data['presion_diastolica']
    frecuencia_cardiaca = data['frecuencia_cardiaca']
    frecuencia_respiratoria = data['frecuencia_respiratoria']
    n_sintomas = data['n_sintomas']

    # Reglas básicas para decisión (sustituir con modelo real en producción)
    if n_sintomas == 0 and temperatura < 37 and frecuencia_cardiaca < 90:
        return "NO ENFERMO"
    elif n_sintomas <= 2 and temperatura < 38:
        return "ENFERMEDAD LEVE"
    elif temperatura >= 38 or frecuencia_cardiaca >= 110 or presion_sistolica < 90:
        return "ENFERMEDAD AGUDA"
    elif n_sintomas >= 3 and presion_diastolica > 90 and frecuencia_respiratoria > 20:
        return "ENFERMEDAD CRÓNICA"
    else:
        return "ENFERMEDAD LEVE"

# Interfaz en Streamlit
st.title("Sistema de Predicción de Enfermedades")
st.write("Ingresa los datos clínicos del paciente para evaluar su estado de salud.")

# Entradas del usuario
edad = st.number_input("Edad del paciente", min_value=0, max_value=120, value=30)
sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
temperatura = st.slider("Temperatura corporal (°C)", 35.0, 42.0, 37.0)
presion_sistolica = st.slider("Presión sistólica (mmHg)", 80, 200, 120)
presion_diastolica = st.slider("Presión diastólica (mmHg)", 50, 130, 80)
frecuencia_cardiaca = st.slider("Frecuencia cardiaca (lpm)", 40, 180, 75)
frecuencia_respiratoria = st.slider("Frecuencia respiratoria (rpm)", 10, 40, 18)
sintomas = st.multiselect("Seleccione los síntomas presentes", [
    "Fiebre", "Tos", "Dolor de cabeza", "Dificultad para respirar",
    "Fatiga", "Dolor muscular", "Náuseas", "Diarrea"])

# Botón de predicción
if st.button("Evaluar estado de salud"):
    # Preprocesamiento de los datos
    data = {
        "edad": edad,
        "sexo": 1 if sexo == "Femenino" else 0,
        "temperatura": temperatura,
        "presion_sistolica": presion_sistolica,
        "presion_diastolica": presion_diastolica,
        "frecuencia_cardiaca": frecuencia_cardiaca,
        "frecuencia_respiratoria": frecuencia_respiratoria,
        "n_sintomas": len(sintomas)
    }

    # Llamada al modelo
    resultado = modelo_simulado(data)

    # Mostrar resultado
    st.subheader("Resultado del análisis médico")
    st.success(f"Estado del paciente: {resultado}")
