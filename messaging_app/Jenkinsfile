pipeline {
    agent any

    environment {
        // Use Jenkins Credentials Manager (add a credential with ID 'github-creds')
        GIT_CREDENTIALS = credentials('github-creds')
         APP_DIR = "messaging-app"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Kizito1990/alx-backend-python.git',
                    credentialsId: "${GIT_CREDENTIALS}"
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source venv/bin/activate
                pytest --junitxml=pytest-report.xml
                '''
            }
        }

        stage('Publish Test Report') {
            steps {
                junit 'pytest-report.xml'
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace...'
            deleteDir()
        }
        success {
            echo 'Pipeline completed successfully 🎉'
        }
        failure {
            echo 'Pipeline failed '
        }
    }
}
