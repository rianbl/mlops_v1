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

# Configurar as URIs do MLflow
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_registry_uri("http://mlflow:5000")

# No topo do arquivo Flask
model_info = {"name": None, "version": None}

def wait_for_model_availability(model_name="RandomForest", stage="Production", timeout=300, poll_interval=10):
    from mlflow.tracking import MlflowClient
    client = MlflowClient()
    elapsed = 0
    while elapsed < timeout:
        try:
            logger.info(f"Verificando disponibilidade do modelo '{model_name}' no estágio '{stage}'...")
            versions = client.get_latest_versions(model_name, [stage])
            if versions:
                version = versions[0].version
                model_uri = f"models:/{model_name}/{stage}"
                loaded_model = mlflow.pyfunc.load_model(model_uri)
                
                # Atualiza as informações do modelo globalmente
                global model_info
                model_info = {
                    "name": model_name,
                    "version": version
                }
                
                logger.info(f"Modelo encontrado: {model_info}")
                return loaded_model
        except Exception as e:
            logger.warning(f"Erro ao verificar modelo: {e}")
        logger.info(f"Aguardando {poll_interval}s antes da próxima verificação...")
        time.sleep(poll_interval)
        elapsed += poll_interval
    logger.critical(f"Timeout ao aguardar o modelo '{model_name}' no estágio '{stage}'.")
    return None

# Carregar o modelo ao iniciar
model = wait_for_model_availability()

# Endpoint para fornecer informações do modelo atual
@app.route("/model-info")
def get_model_info():
    return jsonify(model_info)

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

# Novo endpoint para recarregar o modelo
@app.route("/reload-model", methods=["POST"])
def reload_model():
    global model
    try:
        logger.info("Recarregando modelo a partir do MLflow...")
        new_model = wait_for_model_availability()
        if new_model is None:
            return jsonify({"error": "New model not available"}), 500
        model = new_model
        logger.info("Modelo recarregado com sucesso.")
        return jsonify({"message": "Model reloaded successfully"}), 200
    except Exception as e:
        logger.error(f"Erro ao recarregar modelo: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
