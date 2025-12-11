pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('SONAR_AUTH_TOKEN')
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
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.token=${SONARQUBE}
                        """
                    }
                }
            }
        }

        stage('OWASP ZAP Scan') {
            steps {
                script {
                    sh 'mkdir -p zap-reports'
                    sh 'chmod -R 777 zap-reports'
                    sh '''
                        echo "[INFO] Starting OWASP ZAP baseline scan..."
                        docker run --rm --network host \
                            -v "$PWD/zap-reports:/zap/wrk/" \
                            ghcr.io/zaproxy/zaproxy:stable \
                            zap-baseline.py -t http://localhost:8081 -r zap-report.html -I
                    '''
                }
            }
        }

        stage('Dependency-Check') {
            steps {
                script {
                    sh 'mkdir -p dependency-check-reports'
                    sh 'chmod -R 777 dependency-check-reports || true'
                    sh '''
                        docker run --rm -v "$PWD":/src owasp/dependency-check:latest \
                          --scan /src \
                          --format ALL \
                          --project "DevSecOps" \
                          --out /src/dependency-check-reports
                    '''
                    archiveArtifacts artifacts: 'dependency-check-reports/**', fingerprint: true
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Cleaning workspace..."
        }
    }
}
