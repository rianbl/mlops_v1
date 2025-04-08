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
          sh '''
            if [ $(docker ps -aq -f name=webapp_container) ]; then
              echo 'Removendo o container existente do WebApp...'
              docker rm -f webapp_container
            fi
            echo 'Iniciando um novo container do WebApp...'
            docker-compose up -d webapp
          '''
        }
      }
    }
  }
}
