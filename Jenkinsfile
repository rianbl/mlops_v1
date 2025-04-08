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
    stage('Restart WebApp') {
      steps {
        script {
          echo 'Reiniciando o container do WebApp para carregar o novo modelo...'
          sh 'docker-compose up -d --force-recreate webapp'
        }
      }
    }
  }
}
