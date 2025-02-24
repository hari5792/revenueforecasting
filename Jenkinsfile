pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "hariharasudhan313/revenueforecast"
        CONTAINER_NAME = "revenueforecast_container"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/hari5792/revenueforecasting.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t %DOCKER_IMAGE% ."
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    bat """
                        docker stop %CONTAINER_NAME% || true
                        docker rm %CONTAINER_NAME% || true
                        docker run -d -p 8501:8501 --name %CONTAINER_NAME% %DOCKER_IMAGE%
                    """
                }
            }
        }
    }
}
