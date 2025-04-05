import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import watermark

# Set MLflow tracking URI (optional if already provided via environment)
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("IrisModelTraining")

with mlflow.start_run() as run:
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)
    
    # Load dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log package versions as parameter
    version_info = watermark.watermark(packages="numpy,scipy,pandas,scikit-learn")
    mlflow.log_param("package_versions", version_info)
    
    # Log the model and register it in MLflow Model Registry
    mlflow.sklearn.log_model(model, "model", registered_model_name="RandomForestIrisModel")
    
    print("MLflow run completed. Run ID:", run.info.run_id)
