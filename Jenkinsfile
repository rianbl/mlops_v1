pipeline {
  agent any
  environment {
    GITHUB_TOKEN = credentials('github-token')
  }
  stages {
    stage('Retraining Model') {
      steps {
        script {
          echo 'Iniciando retreinamento do modelo com autenticação GitHub configurada...'
          sh 'docker-compose run --rm model python model_script.py'
        }
      }
    }
    stage('Restart WebApp') {
      steps {
        script {
          echo 'Reiniciando o container do WebApp para carregar o novo modelo...'
          sh 'docker-compose restart webapp'
        }
      }
    }
  }
}
