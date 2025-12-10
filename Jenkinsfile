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

        stage('OWASP ZAP Scan') {
            steps {
                script {
                    sh """
                    echo '[INFO] Starting OWASP ZAP baseline scan...'

                    docker run --rm --network host \
                        -v ${WORKSPACE}/zap-reports:/zap/wrk/ \
                        ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
                        -t http://localhost:8081 \
                        -r zap-report.html \
                        -J zap.yaml

                    echo '[INFO] ZAP Scan completed. Report saved in zap-reports/zap-report.html'
                    """
                }
            }
        }
    }
}
