pipeline {
  agent any
  stages {
    stage('Retraining Model') {
      steps {
        script {
          echo 'Iniciando processo de retreinamento do modelo...'
          // Executa o script de treinamento no container "model" (sem subir dependências)
          sh 'docker-compose run --rm --no-deps model python model_script.py'
        }
      }
    }
    stage('Restart WebApp') {
      steps {
        script {
          echo 'Reiniciando (ou iniciando) o container do WebApp para carregar o novo modelo...'
          // Garante que o serviço webapp esteja ativo, criando-o se necessário
          sh 'docker-compose up -d webapp'
        }
      }
    }
  }
}
