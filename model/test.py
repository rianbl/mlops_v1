import pickle
import numpy as np
import os

# Caminho do modelo salvo
model_path = r"C:\Users\rianb\linux\mlops_v1\models\RandomForest_20250403_160744.pkl"

# Verificar se o arquivo existe
if not os.path.exists(model_path):
    print(f"Erro: O arquivo do modelo '{model_path}' não foi encontrado.")
    exit(1)

# Carregar o modelo salvo
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Criar um exemplo de entrada (substitua conforme necessário)
sample_input = np.array([[2.1, 1.5, 5.4, 2.2]])  # Exemplo do dataset Iris

# Fazer a previsão
prediction = model.predict(sample_input)

# Mostrar a previsão
print("Previsão:", prediction)
