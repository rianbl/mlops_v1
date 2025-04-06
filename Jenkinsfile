pipeline {
  agent any
  stages {
    stage('Start MLflow') {
      steps {
        script {
          echo 'Building and starting the MLflow container...'
          sh 'docker-compose up -d --build mlflow'
        }

      }
    }

    stage('Build and Start Model') {
      steps {
        script {
          echo 'Building and running the model container...'
          sh 'docker-compose up --build model'
        }

      }
    }

    stage('Stop Model Container') {
      steps {
        script {
          echo 'Stopping the model container after execution...'
          sh 'docker stop model_container || true'
        }

      }
    }

    stage('Start WebApp') {
      steps {
        script {
          echo 'Starting the WebApp...'
          sh 'docker-compose up -d --build webapp'
        }

      }
    }

  }
}