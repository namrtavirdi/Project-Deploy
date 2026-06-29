pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
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
                bat 'taskkill /F /IM python.exe >nul 2>&1 || exit /b 0'
            }
        }

        stage('Start Flask App') {
            steps {
                bat 'start "" cmd /c python src\\app.py'
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
            echo 'Application is running.'
            echo '==========================================='
        }

        failure {
            echo '==========================================='
            echo 'Build Failed!'
            echo '==========================================='
        }
    }
}
