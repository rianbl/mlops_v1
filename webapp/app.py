from flask import Flask, request, jsonify, render_template
import mlflow
import mlflow.pyfunc
import numpy as np
import time
import traceback
import logging
import sys
from mlflow.tracking import MlflowClient

app = Flask(__name__)

# Setup do logging para que apareça no terminal do Docker
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Set the MLflow tracking URI
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_registry_uri("http://mlflow:5000")

def wait_for_model_availability(model_name="RandomForestIrisModel", stage="Production", timeout=300, poll_interval=10):
    client = MlflowClient()
    elapsed = 0

    while elapsed < timeout:
        try:
            logger.info(f"Verificando disponibilidade do modelo '{model_name}' no estágio '{stage}'...")
            versions = client.get_latest_versions(model_name, [stage])
            if versions:
                logger.info(f"Modelo encontrado com version: {versions[0].version}.")
                return mlflow.pyfunc.load_model(f"models:/{model_name}/{stage}")
        except Exception as e:
            logger.warning(f"Erro ao verificar modelo: {e}")

        logger.info(f"Aguardando {poll_interval}s antes da próxima verificação...")
        time.sleep(poll_interval)
        elapsed += poll_interval

    logger.critical(f"Timeout ao aguardar o modelo '{model_name}' no estágio '{stage}'.")
    return None

# Uso no início
model = wait_for_model_availability()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        logger.error("Tentativa de previsão sem modelo carregado.")
        return jsonify({"error": "Model not found"}), 500

    try:
        data = request.json
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)[0]
        logger.info(f"Predição realizada com sucesso: {prediction}")
        return jsonify({"prediction": int(prediction)})
    except Exception as e:
        logger.error(f"Erro ao realizar predição: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
