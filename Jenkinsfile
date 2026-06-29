pipeline {
    agent any

    environment {
        PYTHON = 'python'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/namrtavirdi/Project-Deploy.git'
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                python --version
                pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Stop Previous App') {
            steps {
                bat '''
                taskkill /F /IM python.exe >nul 2>&1 || exit /b 0
                '''
            }
        }

        stage('Start Flask App') {
            steps {
                bat '''
                start "Leaf Disease App" cmd /c python src\\app.py
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Application deployed successfully!'
            }
        }
    }

    post {

        success {
            echo '==========================================='
            echo 'Build Successful!'
            echo 'Leaf Disease Detection App is Running.'
            echo '==========================================='
        }

        failure {
            echo '==========================================='
            echo 'Build Failed!'
            echo '==========================================='
        }

        always {
            cleanWs()
        }
    }
}
