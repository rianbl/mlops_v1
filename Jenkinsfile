pipeline {
  agent any
  stages {
    stage('Retraining Model') {
      steps {
        script {
          echo 'Iniciando processo de retreinamento do modelo...'
          sh 'docker-compose run --rm --no-deps model python model_script.py'
        }
      }
    }
    stage('Reload WebApp Model') {
      steps {
        script {
          echo 'Enviando chamada ao endpoint de reload do modelo no WebApp...'
          // Aguarda alguns segundos para garantir que o modelo esteja registrado
          sh 'sleep 10'
          // Use o nome do serviço "webapp" para fazer a chamada, pois "localhost" não apontará para o webapp.
          sh 'curl -X POST http://webapp:5001/reload-model'
        }
      }
    }
  }
}
