import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==========================================
print("Acessando o banco de dados MNIST...")
# Carregando a base de dados MNIST (dígitos de 0 a 9) [cite: 891, 895]
(x_treino_orig, y_treino_orig), (x_teste_orig, y_teste_orig) = datasets.mnist.load_data()

# Separando dados de validação (5.000 registros para o modelo se ajustar durante o treino) [cite: 920]
x_val_orig = x_treino_orig[:5000]
y_val = y_treino_orig[:5000]
x_treino_orig = x_treino_orig[5000:]
y_treino = y_treino_orig[5000:]

# Aplicando Padding (Preenchimento): A LeNet-5 exige entrada 32x32, mas o MNIST é 28x28 [cite: 927, 928]
# Adicionamos uma borda de 2 pixels de zeros (constant) em cada lado [cite: 171]
x_treino_pad = np.pad(x_treino_orig, ((0,0), (2,2), (2,2)), 'constant')
x_val_pad = np.pad(x_val_orig, ((0,0), (2,2), (2,2)), 'constant')
x_teste_pad = np.pad(x_teste_orig, ((0,0), (2,2), (2,2)), 'constant')

# O TensorFlow espera que a imagem tenha o canal de cor. Como é escala de cinza, adicionamos uma dimensão extra "1" [cite: 922]
x_treino_pad = np.expand_dims(x_treino_pad, axis=-1)
x_val_pad = np.expand_dims(x_val_pad, axis=-1)
x_teste_pad = np.expand_dims(x_teste_pad, axis=-1)

# Normalização: Transformando os pixels de 0-255 para uma escala de 0 a 1 [cite: 937, 938]
x_treino = x_treino_pad / 255.0
x_val = x_val_pad / 255.0
x_teste = x_teste_pad / 255.0


# ==========================================
# 2. CONSTRUÇÃO DA ARQUITETURA DA REDE
# ==========================================
print("Montando a arquitetura cibernética (LeNet-5)...")
modelo = models.Sequential()

# Camada 1: Convolução (Extrai características com 6 filtros 5x5) [cite: 641, 642]
modelo.add(layers.Conv2D(6, (5, 5), activation='relu', input_shape=(32, 32, 1)))

# Camada 2: Average Pooling (Comprime e resume a informação) [cite: 644]
modelo.add(layers.AveragePooling2D((2, 2)))

# Camada 3: Convolução (Aprofunda a extração com 16 filtros 5x5) [cite: 646]
modelo.add(layers.Conv2D(16, (5, 5), activation='relu'))

# Camada 4: Average Pooling (Comprime novamente) [cite: 648, 649]
modelo.add(layers.AveragePooling2D((2, 2)))

# Achatamento: Prepara os mapas 2D para a rede neural densa [cite: 961]
modelo.add(layers.Flatten())

# Camadas 5 e 6: Densa / Totalmente Conectada (O "Cérebro" que toma a decisão) [cite: 979]
modelo.add(layers.Dense(120, activation='relu'))
modelo.add(layers.Dense(84, activation='relu'))

# Camada de Saída: 10 neurônios (um para cada dígito) usando Softmax (calcula a probabilidade) [cite: 980, 982]
modelo.add(layers.Dense(10, activation='softmax'))


# ==========================================
# 3. COMPILAÇÃO E TREINAMENTO
# ==========================================
# Configurando como a rede vai aprender e medir seus erros [cite: 995, 1000]
modelo.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print("Iniciando o treinamento (O 'Grind'). Isso pode levar alguns segundos...")
# Treinando o modelo por 10 épocas [cite: 1001]
historico = modelo.fit(x_treino, y_treino,
                       epochs=10,
                       validation_data=(x_val, y_val))


# ==========================================
# 4. AVALIAÇÃO FINAL NO MUNDO REAL
# ==========================================
print("\nTestando o modelo com dados que ele nunca viu...")
erro_teste, acuracia_teste = modelo.evaluate(x_teste, y_teste_orig, verbose=2)

print(f"\n>>> Acurácia Final da Rede: {acuracia_teste*100:.2f}% <<<")