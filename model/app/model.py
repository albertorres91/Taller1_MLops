import numpy as np
from pydantic import BaseModel, Field
from typing import List, Optional

# Lista de diagnósticos posibles actualizada
diagnosis = ['NO ENFERMO', 'ENFERMEDAD LEVE', 'ENFERMEDAD AGUDA', 'ENFERMEDAD CRÓNICA', 'ENFERMEDAD TERMINAL']

# Función sencilla para diagnóstico aleatorio (fallback)
def diag():
    # Genera un diagnóstico aleatorio
    return np.random.choice(diagnosis, 1)

# Implementando la función completa del archivo paste.txt
def clasificar_estado_salud_sin_presion(sintomas, temperatura, edad, sexo, frecuencia_cardiaca):
    """
    Clasifica el estado de salud basado en síntomas, temperatura, edad, sexo y frecuencia cardiaca.
    NO incluye la presión arterial.
    Esta es una simulación y NO debe usarse para diagnóstico médico real.

    Args:
        sintomas (list): Lista de hasta 3 strings describiendo síntomas.
        temperatura (float): Temperatura corporal en grados Celsius.
        edad (int): Edad en años.
        sexo (str): "masculino" o "femenino".
        frecuencia_cardiaca (int): Pulsaciones por minuto.

    Returns:
        str: Etiqueta: "NO ENFERMO", "ENFERMEDAD LEVE", "ENFERMEDAD AGUDA", "ENFERMEDAD CRÓNICA", "ENFERMEDAD TERMINAL".
    """

    # 1. Validar entradas
    if not isinstance(sintomas, list):
        return "Error: Los síntomas deben ser una lista."
    if not isinstance(temperatura, (int, float)):
        return "Error: La temperatura debe ser un número."
    if not isinstance(edad, int) or edad < 0 or edad > 120 :
        return "Error: Edad inválida."
    if not isinstance(sexo, str) or sexo.lower().strip() not in ["masculino", "femenino"]:
        return "Error: Sexo inválido. Usar 'masculino' o 'femenino'."
    if not isinstance(frecuencia_cardiaca, int) or frecuencia_cardiaca < 30 or frecuencia_cardiaca > 250:
         return "Error: Frecuencia cardíaca inválida."

    sintomas_norm = [s.lower().strip() for s in sintomas if isinstance(s, str)]
    sexo_norm = sexo.lower().strip()

    # --- Lógica de decisión basada en condicionales ---

    # Factores de riesgo por edad (simplificado)
    es_vulnerable_edad = (edad < 5 or edad > 65)

    # Umbrales de Frecuencia Cardíaca (muy simplificado)
    fc_normal_alta = 100
    fc_taquicardia_leve = 120
    fc_taquicardia_aguda = 140
    fc_bradicardia_sintomatica = 50 # FC por debajo de la cual, con síntomas, es preocupante

    if edad < 1: # Bebés
        fc_normal_alta = 160
        fc_taquicardia_leve = 180
        fc_taquicardia_aguda = 200
    elif edad < 6: # Niños pequeños
        fc_normal_alta = 140
        fc_taquicardia_leve = 160
        fc_taquicardia_aguda = 180
    elif edad < 12: # Niños
        fc_normal_alta = 120
        fc_taquicardia_leve = 140
        fc_taquicardia_aguda = 160

    # 0. Condiciones para ENFERMEDAD TERMINAL (prioridad máxima si se detectan)
    sintomas_terminales_clave = [
        "cáncer en etapa terminal", 
        "enfermedad terminal diagnosticada",
        "insuficiencia orgánica múltiple",
        "enfermedad degenerativa avanzada",
        "cuidados paliativos"
    ]
    
    tiene_sintoma_terminal = any(st in " ".join(sintomas_norm) for st in sintomas_terminales_clave)
    
    # Pacientes con enfermedades terminales conocidas
    if tiene_sintoma_terminal:
        return "ENFERMEDAD TERMINAL"
    
    # Pacientes con múltiples fallos orgánicos y síntomas graves
    if ("fallo hepático" in sintomas_norm and "fallo renal" in sintomas_norm) or \
       ("fallo cardíaco avanzado" in sintomas_norm and "dificultad extrema para respirar" in sintomas_norm):
        return "ENFERMEDAD TERMINAL"
    
    # Pacientes con metástasis conocida
    if "metástasis" in sintomas_norm and ("dolor crónico severo" in sintomas_norm or "pérdida de peso extrema" in sintomas_norm):
        return "ENFERMEDAD TERMINAL"
    
    # Pacientes con deterioro extremo y edad avanzada
    if edad > 80 and ("deterioro cognitivo avanzado" in sintomas_norm or "incapacidad total" in sintomas_norm) and \
       (frecuencia_cardiaca < 50 or frecuencia_cardiaca > 140) and temperatura < 35.0:
        return "ENFERMEDAD TERMINAL"

    # A. Condiciones para ENFERMEDAD CRÓNICA
    # (Prioridad si se cumplen ciertos criterios, incluso con síntomas agudos leves)
    sintomas_cronicos_clave = ["fatiga persistente", "dolor crónico", "pérdida de peso inexplicable gradual",
                               "asma", "diabetes conocida", "hipertensión diagnosticada",
                               "enfermedad pulmonar obstructiva crónica", "epoc"]
    tiene_sintoma_cronico_clave = any(sc in " ".join(sintomas_norm) for sc in sintomas_cronicos_clave)

    if "hipertensión diagnosticada" in sintomas_norm:
        return "ENFERMEDAD CRÓNICA"
    if "diabetes conocida" in sintomas_norm and ("sed excesiva" in sintomas_norm or "micción frecuente" in sintomas_norm or "visión borrosa gradual" in sintomas_norm):
        return "ENFERMEDAD CRÓNICA"
    if ("asma" in sintomas_norm or "epoc" in sintomas_norm or "enfermedad pulmonar obstructiva crónica" in sintomas_norm) and \
       ("tos frecuente" in sintomas_norm or "dificultad leve para respirar habitual" in sintomas_norm or "sibilancias" in sintomas_norm):
        if temperatura < 38.0: # Menos probable que sea una infección aguda si la fiebre no es alta
            return "ENFERMEDAD CRÓNICA"

    # Edad avanzada con síntomas sugerentes de cronicidad y sin fiebre alta
    if edad > 70 and not (temperatura > 38.5): # Si no hay fiebre alta que sugiera agudo
        if ("fatiga persistente" in sintomas_norm or "dolor crónico articular" in sintomas_norm or "movilidad reducida progresiva" in sintomas_norm) and len(sintomas_norm) >=1:
             return "ENFERMEDAD CRÓNICA"
        # Si tiene 2+ síntomas leves y FC algo alterada, y es mayor.
        if len(sintomas_norm) >= 2 and (frecuencia_cardiaca > fc_normal_alta + 10 or frecuencia_cardiaca < 55):
            sintomas_leves_comunes = ["cansancio", "dolor leve", "malestar general"]
            if any(slc in " ".join(sintomas_norm) for slc in sintomas_leves_comunes):
                return "ENFERMEDAD CRÓNICA" # Podría ser deterioro general crónico

    # B. Condiciones para ENFERMEDAD AGUDA
    sintomas_agudos_clave = ["dificultad para respirar severa", "dolor en el pecho opresivo", "dolor en el pecho irradiado",
                             "confusión aguda", "desorientación súbita", "vómitos persistentes e intensos",
                             "fiebre muy alta", "pérdida de conciencia", "incapacidad para moverse", "convulsiones"]
    tiene_sintoma_agudo_clave = any(sa in " ".join(sintomas_norm) for sa in sintomas_agudos_clave)

    if temperatura >= 39.5 or (es_vulnerable_edad and temperatura >= 39.0): # Fiebre muy alta, o alta en vulnerables
        return "ENFERMEDAD AGUDA"
    if tiene_sintoma_agudo_clave:
        return "ENFERMEDAD AGUDA"
    if frecuencia_cardiaca > fc_taquicardia_aguda: # Taquicardia severa
        if len(sintomas_norm) > 0 or temperatura > 38.0: # Con síntomas o fiebre
             return "ENFERMEDAD AGUDA"
    if frecuencia_cardiaca < fc_bradicardia_sintomatica and ("mareo intenso" in sintomas_norm or "debilidad extrema" in sintomas_norm or "pérdida de conciencia" in sintomas_norm or "confusión" in sintomas_norm): # Bradicardia sintomática
        return "ENFERMEDAD AGUDA"
    # Dolor en el pecho con factores de riesgo/acompañantes (sin presión, se enfoca en FC y edad)
    if ("dolor en el pecho opresivo" in sintomas_norm or "dolor en el pecho irradiado" in sintomas_norm) and \
       (edad > 40 or frecuencia_cardiaca > fc_taquicardia_leve or "sudoración fría" in sintomas_norm or "náuseas intensas" in sintomas_norm):
        return "ENFERMEDAD AGUDA"
    # Vulnerables con múltiples síntomas y vitales alterados
    if es_vulnerable_edad and len(sintomas_norm) >=2 and (temperatura > 38.0 or frecuencia_cardiaca > fc_taquicardia_leve):
        # Chequear que no sean síntomas muy leves que podrían ser crónicos
        if not ("fatiga persistente" in sintomas_norm and temperatura < 38.5): # Evitar clasificar como agudo un crónico leve en anciano
            return "ENFERMEDAD AGUDA"


    # C. Condiciones para ENFERMEDAD LEVE
    sintomas_leves_clave = ["tos", "dolor de garganta", "congestión nasal", "dolor de cabeza leve",
                            "malestar general", "fiebre leve", "dolor muscular leve", "fatiga leve", "estornudos"]
    num_sintomas_leves = sum(1 for s_leve in sintomas_leves_clave if s_leve in " ".join(sintomas_norm))

    if temperatura >= 37.8 and temperatura < 39.0 : # Fiebre leve a moderada (sin ser ya AGUDA por vulnerabilidad)
        if len(sintomas_norm) > 0 or frecuencia_cardiaca > fc_normal_alta : # Cualquier síntoma o FC algo elevada con fiebre
            return "ENFERMEDAD LEVE"

    if num_sintomas_leves >= 1:
        if temperatura > 37.2 or (frecuencia_cardiaca > fc_normal_alta and frecuencia_cardiaca <= fc_taquicardia_leve): # Síntomas leves con ligera alteración de temp/FC
            return "ENFERMEDAD LEVE"
        if num_sintomas_leves >=2: # Múltiples síntomas leves incluso con vitales "normales"
            return "ENFERMEDAD LEVE"

    # Si hay algún síntoma reportado y no es agudo/crónico, y los vitales están levemente alterados
    if len(sintomas_norm) > 0:
        if (temperatura > 37.2 and temperatura < 37.8) or \
           (frecuencia_cardiaca > fc_normal_alta and frecuencia_cardiaca <= fc_taquicardia_leve):
            return "ENFERMEDAD LEVE"


    # D. Condiciones para NO ENFERMO
    if temperatura <= 37.2 and (frecuencia_cardiaca >= fc_bradicardia_sintomatica and frecuencia_cardiaca <= fc_normal_alta):
        if not sintomas_norm: # Sin síntomas y vitales normales
            return "NO ENFERMO"
        if len(sintomas_norm) == 1 and ("cansancio ligero puntual" in sintomas_norm or "un poco de sueño" in sintomas_norm):
            return "NO ENFERMO"

    # Fallback: Si hay síntomas pero no encajan claramente y no es NO ENFERMO, asumimos LEVE
    if len(sintomas_norm) > 0:
        return "ENFERMEDAD LEVE"

    return "NO ENFERMO"