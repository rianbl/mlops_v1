import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import watermark
from mlflow.tracking import MlflowClient

# Set MLflow tracking URI (optional if already provided via environment)
mlflow.set_registry_uri("http://mlflow:5000")
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("Model_Experiment")

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
    mlflow.sklearn.log_model(model, "model", registered_model_name="RandomForest")
    
    print("MLflow run completed. Run ID:", run.info.run_id)

    # Promote the latest model version to Production
    client = MlflowClient(tracking_uri="http://mlflow:5000")
    latest_versions = client.get_latest_versions("RandomForest")
    if latest_versions:
        version_to_promote = latest_versions[0].version
        client.transition_model_version_stage(
            name="RandomForest",
            version=version_to_promote,
            stage="Production",
            archive_existing_versions=True
        )
        print(f"Promoted model version {version_to_promote} to Production.")
    else:
        print("No versions found for the registered model.")
