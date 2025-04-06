from flask import Flask, request, jsonify, render_template
import mlflow
import mlflow.pyfunc
import numpy as np

app = Flask(__name__)

# Set the MLflow tracking URI (optional, if not set via environment)
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_registry_uri("http://mlflow:5000")

def load_registered_model():
    try:
        # Load the model from the MLflow Model Registry.
        # Make sure the model "RandomForestIrisModel" is promoted to the "Production" stage.
        model_uri = "models:/RandomForestIrisModel/Production"
        model = mlflow.pyfunc.load_model(model_uri)
        return model
    except Exception as e:
        print(f"Error loading model from MLflow: {e}")
        return None

# Load the model from MLflow
model = load_registered_model()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not found"}), 500

    try:
        data = request.json
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)[0]
        return jsonify({"prediction": int(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
