pipeline {
    agent any

    environment {
        SONARQUBE_URL = "http://localhost:9000"
    }

    stages {

        stage('SCM') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    script {
                        def scannerHome = tool 'sonar-scanner'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=DevSecOps \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=${SONARQUBE_URL} \
                                -Dsonar.token=$SONAR_TOKEN
                        """
                    }
                }
            }
        }

        stage('OWASP ZAP Scan') {
            steps {
                script {
                    echo "[INFO] Starting OWASP ZAP baseline scan..."

                    sh """
                        docker run --rm --network host \
                            -v \$WORKSPACE/zap-reports:/zap/wrk \
                            ghcr.io/zaproxy/zaproxy:stable \
                            zap-baseline.py \
                            --autooff \
                            -t http://localhost:8081 \
                            -r zap-report.html
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Cleaning workspace..."
        }
        failure {
            echo "Pipeline failed! Check logs."
        }
    }
}
