pipeline {
  agent any
  stages {
    stage('Retraining Model') {
      steps {
        script {
          echo 'Iniciando processo de retreinamento do modelo...'
          // Executa o script de treinamento no container "model" e espera seu término.
          sh 'docker-compose run --rm model python model_script.py'
        }
      }
    }
    stage('Restart WebApp') {
      steps {
        script {
          echo 'Reiniciando o container do WebApp para carregar o novo modelo...'
          // Reinicia o container do webapp para que ele carregue a nova versão do modelo.
          sh 'docker-compose restart webapp'
        }
      }
    }
  }
}
