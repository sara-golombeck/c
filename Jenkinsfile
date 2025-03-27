pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python:3.11-slim'  
        CONTAINER_NAME = 'pytest-container'
    }



    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t my-python-tests .'
                }
            }
        }

        stage('Run Tests with Pytest in Docker') {
            steps {
                script {
                    sh """
                        docker run --rm -v \$(pwd):/app my-python-tests
                    """
                }
            }
        }

        stage('Archive Test Results') {
            steps {
                junit '**/tests/results/*.xml'  
            }
        }
    }

    post {
        always {
            sh 'docker ps -a -q --filter "name=${CONTAINER_NAME}" | xargs --no-run-if-empty docker rm'
        }
    }
}
