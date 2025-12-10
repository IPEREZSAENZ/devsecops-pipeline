pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('SONAR_AUTH_TOKEN')
        SONAR_HOST  = 'http://localhost:9000'
    }

    stages {
        stage('SCM') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'
                    withEnv(["PATH=${scannerHome}/bin:${env.PATH}"]) {
                        sh """
                            sonar-scanner \
                            -Dsonar.projectKey=DevSecOps \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST} \
                            -Dsonar.login=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }
    }
}
