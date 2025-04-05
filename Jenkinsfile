pipeline {
  agent any
  stages {
    stage('Build e Start Model') {
      steps {
        script {
          echo 'Construindo e rodando o container do modelo...'
          sh 'docker-compose up --build model'
        }
      }
    }

    stage('Parar Model Container') {
      steps {
        script {
          echo 'Parando o container do modelo após execução...'
          sh 'docker stop model_container || true'
        }
      }
    }

    stage('Verificar existência da pasta de logs') {
      steps {
        script {
          echo 'Verificando se a pasta ./model/logs existe no host...'
          sh 'sleep 5'
          sh 'ls -l ./model/logs || echo "logs ainda nao existem"'
        }
      }
    }

    stage('Start WebApp') {
      steps {
        script {
          echo 'Iniciando o WebApp...'
          sh 'docker-compose up -d --build webapp'
        }
      }
    }
  }
}
