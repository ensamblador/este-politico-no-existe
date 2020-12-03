# Este político no existe

## Repositorio de apoyo y reproducibilidad de experimentos 
### Magister DataScience
### Universidad del Desarrollo

Los modelos de lenguaje natural han adquirido una gran relevancia desde 2018 desde la incorporación de la arquitectura Transformer. Aunque existe una gran cantidad y muy diversos trabajos al respecto, muy poco podemos encontrar en español. 


Este trabajo aborda una aplicación del modelo GPT-2, una implementación de arquitectura transformer, para ejecutar tareas de generación de texto casual y texto controlado. En ambos casos hemos realizado el entrenamiento con las publicaciones de las autoridades políticas chilenas en la red social twitter.


Los resultados muestran que incluso un modelo GPT-2 base puede ser ajustado para cumplir una tarea específica como generar nuevos Tweets políticos reutilizando el aprendizaje del lenguage pre entrenado. Además entrenamos el modelo para que aprenda de los contextos de cada uno de los tweets y utilizar estos mismos contextos para solicitar la generación de acuerdo a parámetros de control. 
Las aplicaciones de estos nuevos modelos de lenguaje con atención están en la vida personal como en el mundo empresarial. Usando estas innovaciones es posible agregar más valor a servicios actuales o crear nuevos servicios, habilitados con esta tecnología.


En este trabajo implementamos un modelo de generación de texto casual GPT-2 en español y, como una tarea específica, le hemos enseñado a generar tweets como una autoridad política chilena. En cuanto a la generación de texto, le instruimos de cuál tema hablar y con qué sentimiento, poniendo en práctica una técnica para controlar el contenido de esta síntesis.


### Experimentos

1. [Ajuste fino de gpt2 con tweets](ajuste-fino-gpt2-tweets)

En este experimento entrenamos un modelo GPT-2 para una tarea específica de twittear como un político chileno, también hicimos el experimento de dividir los set de datos de izquierda y derecha para entrenar dos modelos diferentes. Un politico de izquierda y otro de derecha que generan nuevos tweets con su color politico.

1. [Entrenamiento de un modelo GPT-2 con Wikipedia en Español](train-gpt2-es)

En este experimento entrenamos un modelo GPT-2 custom utilizando un set de datos de español con el objetivo de generar textos casuales a partir de un prompt. Tambien utilizamos este modelo en los experimentos del punto anterior.

1. [Entrenamiendo para la generación controlada de textos (usando temas y palabras claves) ](contextual-training)

Lo que hicimos acá fue modificar y reprocesar el set de datos para entrenar el modelo utilizando un contexto (entidades, coalición política, partido, sentimiento y palabras claves) De tal forma de que el modelo pudiese entender qué significa este contexto el tuit generado.

El resultado de todo esto es que tenemos un modelo que puede sintetizar nuevo tuit en base a parámetros tales como coalición, partido, sentimiento, entidades y palabras claves.


### Modelos transformers entrenados en esta tesis y disponibles:

* [GPT-2 entrenado para la generación casual de texto expañol](https://huggingface.co/ensamblador/gpt2-es-48heads)

* [GPT-2 más simple (16 heads, 512 pos) para texto casual español](https://huggingface.co/ensamblador/gpt2_espanol_8hx512pos)

* [GPT-2 (48 heads) Entrenado con tweets de derecha](https://huggingface.co/ensamblador/gpt2-derecha-with-bos-eos-48heads)


___

* [Modelo GPT2 Entrenado para generar textos controlados de políticos](https://huggingface.co/ensamblador/gpt2-twitter-politico)
___

### Uso de los modelos:

Ejemplo: Para utilizar estos modelos ya sea en Tensorflow o PyTorch basta con importarlos utilizando la librería transformers (`pip install transformers`)
```python 
from transformers import AutoTokenizer, AutoModelWithLMHead
tokenizer = AutoTokenizer.from_pretrained("ensamblador/gpt2-es-48heads")
model = AutoModelWithLMHead.from_pretrained("ensamblador/gpt2-es-48heads")

input_context = "Nos encontramos "
input_ids = tokenizer(input_context, return_tensors="pt")
outputs = model.generate(input_ids=input_ids, max_length=20, do_sample=True)

print("Generated:", tokenizer.decode(outputs[0],skip_special_tokens=True))
```
```terminal
>> nos encontramos en la zona de la laguna de los Patos, en la zona de la laguna de Aculeo donde algunos vecinos...
```

