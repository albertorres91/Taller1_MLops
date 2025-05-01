import numpy as np

diagnosis = ['NO ENFERMO', 'ENFERMEDAD LEVE','ENFERMEDAD AGUDA','ENFERMEDAD CRÓNICA']

def diag():
    
    # Genera un diagnóstico aleatorio
    # Se elige un diagnóstico aleatorio de la lista de diagnósticos
    # y se devuelve como resultado.
    return np.random.choice(diagnosis,1)
