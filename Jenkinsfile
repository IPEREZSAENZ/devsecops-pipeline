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
                              -Dsonar.token=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }

        stage('OWASP ZAP Scan') {
            steps {
                sh "mkdir -p zap-reports"
                sh "chmod -R 777 zap-reports"

                sh """
                    docker run --rm --network host \
                      -v ${WORKSPACE}/zap-reports:/zap/wrk \
                      ghcr.io/zaproxy/zaproxy:stable \
                      zap-baseline.py -t http://localhost:8081 -r zap-report.html -I
                """
            }
            post {
                always {
                    publishHTML([
                        reportDir: 'zap-reports',
                        reportFiles: 'zap-report.html',
                        reportName: 'ZAP Security Report',
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true
                    ])
                }
            }
        }

        /* ===========================
           DEPENDENCY CHECK (FIX FINAL)
           =========================== */
        stage('Dependency Check') {
            steps {
                script {
                    // Dependency-Check instalado como Tool en Jenkins
                    def dcHome = tool 'DC'

                    sh "mkdir -p dependency-check-reports"

                    sh """
                        ${dcHome}/bin/dependency-check.sh \
                          --project "DevSecOps" \
                          --scan . \
                          --format HTML \
                          --out dependency-check-reports \
                          --enableExperimental \
                          --enableRetired \
                          --failOnCVSS 11
                          --noupdate                          
                    """
                }
            }
            post {
                always {
                    publishHTML([
                        reportDir: 'dependency-check-reports',
                        reportFiles: 'dependency-check-report.html',
                        reportName: 'Dependency-Check Report',
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true
                    ])
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}

