import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import watermark
from mlflow.tracking import MlflowClient

# Configurar MLflow: tracking e registry apontando para o serviço mlflow
mlflow.set_registry_uri("http://mlflow:5000")
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("Model_Experiment")

with mlflow.start_run() as run:
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)
    
    # Carregar dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Dividir dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Treinar o modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Avaliar o modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)
    
    # Logar as versões dos pacotes
    version_info = watermark.watermark(packages="numpy,scipy,pandas,scikit-learn")
    mlflow.log_param("package_versions", version_info)
    
    # Logar o modelo e registrar no Model Registry
    mlflow.sklearn.log_model(model, "model", registered_model_name="RandomForest")
    
    print("MLflow run completed. Run ID:", run.info.run_id)

    # Promover a nova versão do modelo para Production  
    client = MlflowClient(tracking_uri="http://mlflow:5000")
    # Usando search_model_versions para retornar todas as versões do modelo
    versions = client.search_model_versions("name='RandomForest'")
    if versions:
        # Ordenar as versões de forma decrescente (maior version é a mais nova)
        versions_sorted = sorted(versions, key=lambda v: int(v.version), reverse=True)
        version_to_promote = versions_sorted[0].version
        client.transition_model_version_stage(
            name="RandomForest",
            version=version_to_promote,
            stage="Production",
            archive_existing_versions=True
        )
        print(f"Promoted model version {version_to_promote} to Production.")
    else:
        print("No versions found for the registered model.")
