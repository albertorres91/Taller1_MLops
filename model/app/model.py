import numpy as np

diagnosis = ['SANO', 'ENFERMEDAD LEVE','ENFERMEDAD GRAVE','ENFERMEDAD CRÓNICA', 'ENFERMEDAD HUÉRFANA']

def diag():
    
    # Genera un diagnóstico aleatorio
    # Se elige un diagnóstico aleatorio de la lista de diagnósticos
    # y se devuelve como resultado.
    return np.random.choice(diagnosis,1)
