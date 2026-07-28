pipeline {
    agent any

    environment {
        BUILD_VERSION = "1.0.${BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = "portfolio-cicd-${BUILD_NUMBER}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build and Test') {
            parallel {
                stage('Java 17') {
                    agent { docker { image 'maven:3.9.9-eclipse-temurin-17'; args '-v $HOME/.m2:/root/.m2' } }
                    steps { dir('java-order-service') { sh 'mvn -B clean verify' } }
                    post { always { junit 'java-order-service/target/surefire-reports/*.xml' } }
                }
                stage('Java 21 Compatibility') {
                    agent { docker { image 'maven:3.9.9-eclipse-temurin-21'; args '-v $HOME/.m2:/root/.m2' } }
                    steps { dir('java-order-service') { sh 'mvn -B test' } }
                }
                stage('Python 3.11') {
                    agent { docker { image 'python:3.11-slim' } }
                    steps {
                        dir('python-risk-service') {
                            sh 'pip install -r requirements-dev.txt'
                            sh 'ruff check . && ruff format --check .'
                            sh 'mypy app'
                            sh 'pytest --junitxml=test-results-311.xml'
                        }
                    }
                    post { always { junit 'python-risk-service/test-results-311.xml' } }
                }
                stage('Python 3.12') {
                    agent { docker { image 'python:3.12-slim' } }
                    steps {
                        dir('python-risk-service') {
                            sh 'pip install -r requirements-dev.txt'
                            sh 'pytest --junitxml=test-results-312.xml'
                        }
                    }
                    post { always { junit 'python-risk-service/test-results-312.xml' } }
                }
            }
        }

        stage('Build Versioned Images') {
            steps { sh 'docker compose build' }
        }

        stage('Integration Test') {
            steps {
                sh 'docker compose up -d --wait'
                sh './scripts/integration-test.sh'
            }
            post { always { sh 'docker compose down -v --remove-orphans' } }
        }

        stage('Publish Images') {
            when { branch 'main' }
            steps {
                echo "Production configuration would authenticate to a container registry here."
                sh 'docker image inspect portfolio/order-service:${BUILD_VERSION} >/dev/null'
                sh 'docker image inspect portfolio/risk-service:${BUILD_VERSION} >/dev/null'
            }
        }

        stage('Deploy') {
            when { buildingTag() }
            input { message 'Deploy this tagged release?'; ok 'Deploy' }
            steps { echo "Deploying release ${TAG_NAME}" }
        }
    }

    post {
        always { cleanWs() }
        success { echo "Pipeline ${BUILD_VERSION} completed successfully." }
        failure { echo 'Pipeline failed. Review the stage logs and test reports.' }
    }
}
