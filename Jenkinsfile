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
          // Faz uma requisição POST para o endpoint /reload-model
          sh 'curl -X POST http://localhost:5001/reload-model'
        }
      }
    }
  }
}
