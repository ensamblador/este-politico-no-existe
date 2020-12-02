# Este político no existe
Para el experimento realizamos el entrenamiento del modelo y tokenizador . Utilizando un corpus de Wikipedia 4.8 GB de datos (más de mil millones de palabras)  entrenamos un Tokenizador (GPT2Tokenizer) y posteriormente un modelo GPT-2 Para la generación de lenguaje casual (GPT2LMHeadModel) disponibles en librería transformers en  Tensorflow y Pytorch. 

**GPT2LMHeadModel** es un modelo transformer con un cabezal de modelamiento de lenguaje al final, es decir devuelve un vector con probabilidades de elementos del vocabulario (tokens) de un largo parametrizable n_ctx. 

Entrenamos el modelo utilizando un largo máximo de 512 tokens (n_positions=n_ctx=512) y 16 cabezales de atención (n_heads=16) la arquitectura utilizada de 12 capas interiores (n_layer=12) y dimensionalidad interna de 768 (n_embd=768). 
El modelo se entrenó a 5 epochs utilizando 4 GPU en paralelo (Tesla V100) con un tamaño de lote de 16 por GPU. El proceso total tuvo una duración de 45.42 horas.

### Notebooks con los pasos

1. [Ajuste fino de gpt2 con tweets](1-batch-dataset.ipynb)
1. [Creación y entrenamiento del tokenizador](2-batch-tokenise.ipynb)
1. [Entrenamiendo del modelo GPT2 a español](3-train-parallel-third.ipynb)
1. [Pruebas de Generación](4-test.ipynb)
1. [Guardado del modelo Tensorflow en PyTorch](5-save-pytorch-also.ipynb)