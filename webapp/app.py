from flask import Flask, request, jsonify, render_template
import mlflow
import mlflow.pyfunc
import numpy as np
import time
import traceback
import logging
import sys

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

def load_registered_model(retries=5, delay=5):
    model_uri = "models:/RandomForestIrisModel/Production"

    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Tentativa {attempt} de {retries} para carregar o modelo...")
            model = mlflow.pyfunc.load_model(model_uri)
            logger.info("Modelo carregado com sucesso.")
            return model
        except Exception as e:
            logger.error(f"Falha ao carregar modelo na tentativa {attempt}: {e}")
            logger.error(traceback.format_exc())
            if attempt < retries:
                wait = delay * attempt
                logger.info(f"Aguardando {wait} segundos antes da próxima tentativa...")
                time.sleep(wait)
            else:
                logger.critical("Todas as tentativas de carregar o modelo falharam.")
    return None

# Load the model from MLflow
model = load_registered_model()

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
