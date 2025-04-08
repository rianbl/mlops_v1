#!/bin/sh

# Aguarda o MinIO estar pronto
sleep 10

mc alias set minio http://minio:9000 mlflow mlflow123
mc mb --ignore-existing minio/mlflow-artifacts
mc policy set none minio/mlflow-artifacts

