# Taller 1 MLOps -> V1.0

## Caso de estudio
### Antecedentes

Dados los avances tecnológicos, en el campo de la medicina la cantidad de información que existe de los pacientes es muy abundante. Sin embargo, para algunas enfermedades no tan comunes, llamadas huérfanas, los datos que existen escasean. Se requiere construir un modelo que sea capaz de predecir, dados los datos de síntomas de un paciente, si es posible o no que este sufra de alguna enfermedad. Esto se requiere tanto para enfermedades comunes (muchos datos) como para enfermedades huérfanas (pocos datos). 

## Definición del problema

### Entrenamiento del modelo

El modelo será entrenado manualmente por un ingeniero de ML.

El dataset de entrenamiento [link](https://www.kaggle.com/datasets/uom190346a/disease-symptoms-and-patient-profile-dataset/data) tiene síntomas asociados a las enfermedades.

Los datos serán evaluados en un Análisis Exploratorio de Datos (EDA) para identificar su estructura interna. Se entrenarán varios modelos de clasificación y se escogerá el que mejor desempeño tenga, asegurando así el mejor rendimiento.

### Tarea de predicción

El conjunto se pondrá a disposición 24hrs. 7 días a la semana para su consulta. Esto teniendo en cuenta que el servicio está pensado para ayudar al diágnostico médico, quienes, a su vez, trabajan en turnos que cubren la totalidad del día todos los días.

---

### Parte 1: diseño del pipeline de ML

Se propone el siguiente diagrama de pipeline para el problema en cuestión:

[ML_Pipeline]()

