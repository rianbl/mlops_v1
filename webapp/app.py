from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import os

app = Flask(__name__)

# Buscar o modelo salvo mais recente
model_dir = "/app/models"
model_files = sorted([f for f in os.listdir(model_dir) if f.endswith(".pkl")], reverse=True)
if model_files:
    model_path = os.path.join(model_dir, model_files[0])
    with open(model_path, "rb") as f:
        model = pickle.load(f)
else:
    model = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Modelo não encontrado"}), 500

    try:
        data = request.json
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)[0]
        return jsonify({"prediction": int(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
