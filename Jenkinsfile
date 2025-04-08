pipeline {
  agent any
  stages {
    stage('Build Model Image') {
      steps {
        script {
          echo '🔧 (Re)build da imagem do modelo...'
          sh 'docker-compose build model'
        }
      }
    }
    stage('Retraining Model') {
      steps {
        script {
          echo '🤖 Iniciando processo de retreinamento do modelo...'
          sh 'docker-compose run --rm --no-deps model python model_script.py'
        }
      }
    }
    stage('Reload WebApp Model') {
      steps {
        script {
          echo '🔄 Enviando chamada ao endpoint de reload do modelo no WebApp...'
          sh 'sleep 10'
          sh 'curl -X POST http://webapp:5001/reload-model'
        }
      }
    }
  }
}
