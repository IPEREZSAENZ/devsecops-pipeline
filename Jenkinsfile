pipeline {
    agent any

    environment {
        SONARQUBE_URL = "http://localhost:9000" 
        SONARQUBE_SCANNER = "sonar-scanner"
    }

    stages {

        /* --- 1. SCM Checkout --- */
        stage('SCM') {
            steps {
                checkout scm
            }
        }

        /* --- 2. Análisis SAST con SonarQube --- */
        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    script {
                        def scannerHome = tool SONARQUBE_SCANNER

                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=DevSecOps \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONARQUBE_URL} \
                            -Dsonar.token=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }

        /* --- 3. Análisis DAST con OWASP ZAP --- */
        stage('OWASP ZAP Scan') {
            steps {
                script {

                    sh """
                    echo '[INFO] Starting OWASP ZAP baseline scan...'

                    docker run --rm --network host \
                        -v ${WORKSPACE}/zap-reports:/zap/wrk/ \
                        ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
                        -t http://localhost:8081 \
                        -r zap-report.html

                    echo '[INFO] ZAP Scan completed. Report saved in zap-reports/zap-report.html'
                    """
                }
            }
        }

    }

    post {
        always {
            echo "Pipeline finished. Cleaning workspace..."
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed! Check logs."
        }
    }
}
