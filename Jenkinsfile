pipeline {
    agent any

    environment {
        // Optional: Set up a Python virtual environment if needed
        VIRTUAL_ENV = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your repository
                checkout scm
            }
        }

        stage('Set up Python Environment') {
            steps {
                script {
                    // Optional: Set up a virtual environment if required
                    if (!fileExists(VIRTUAL_ENV)) {
                        sh 'python3 -m venv venv'
                    }
                    // Activate the virtual environment
                    sh 'source venv/bin/activate'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Install dependencies (e.g., requirements.txt)
                    sh 'source venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests with Pytest') {
            steps {
                script {
                    // Run pytest to execute your tests
                    sh 'source venv/bin/activate && pytest --maxfail=5 --disable-warnings'
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
           
            sh 'deactivate || true'
        }
    }
}
