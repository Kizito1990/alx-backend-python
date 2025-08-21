pipeline {
    agent any

    environment {
        // GitHub credentials (stored in Jenkins)
        GIT_CREDENTIALS = 'github-creds'

        // Docker Hub repository (change to your username/repo)
        DOCKERHUB_REPO = "ibirikambiri/messaging-app"

        // Docker Hub credentials (stored in Jenkins)
        DOCKER_CREDENTIALS = 'dockedockerhub-credentials'

        // Project directory
        APP_DIR = "messaging_app"
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
                dir("${APP_DIR}") {
                    sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir("${APP_DIR}") {
                    sh '''
                    source venv/bin/activate
                    pytest --junitxml=pytest-report.xml
                    '''
                }
            }
        }

        stage('Publish Test Report') {
            steps {
                dir("${APP_DIR}") {
                    junit 'pytest-report.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dir("${APP_DIR}") {
                        docker.build("${DOCKERHUB_REPO}:latest")
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS}") {
                        docker.image("${DOCKERHUB_REPO}:latest").push()
                    }
                }
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
            echo 'Pipeline failed ❌'
        }
    }
}
