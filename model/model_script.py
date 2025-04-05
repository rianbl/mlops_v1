import os
import logging
import pickle
from datetime import datetime
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import watermark

# Criar diretórios se não existirem
os.makedirs("/app/models", exist_ok=True)
os.makedirs("/app/logs", exist_ok=True)

# Criar timestamps
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Configuração do logger para o treinamento
train_log_path = f"/app/logs/train_{timestamp}.log"
logging.basicConfig(filename=train_log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carregar dataset
logging.info("Carregando o dataset Iris.")
iris = load_iris()
X, y = iris.data, iris.target

# Dividir dataset
logging.info("Dividindo o dataset em treino e teste.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
logging.info("Treinando o modelo RandomForest.")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Avaliação
logging.info("Testando o modelo.")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
logging.info(f"Acurácia do modelo: {accuracy:.4f}")

# Configuração do logger para registrar as versões dos pacotes
package_log_path = "/app/logs/package_versions.log"
logging.basicConfig(filename=package_log_path, level=logging.INFO, format="%(message)s")

# Registrar versões dos pacotes
version_info = watermark.watermark(packages="numpy,scipy,pandas,scikit-learn")
logging.info(version_info)
print("\n" + version_info)
logging.info("Versões dos pacotes registradas.")

# Salvar modelo
model_filename = f"RandomForest_{timestamp}.pkl"
model_path = f"/app/models/{model_filename}"
logging.info(f"Salvando o modelo em {model_path}.")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

logging.info("Processo finalizado com sucesso.")
