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

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-password', variable: 'DOCKER_PASS')]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u hariharasudhan313 --password-stdin
                        docker push %DOCKER_IMAGE%
                    """
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    bat """
                        docker stop %CONTAINER_NAME% || exit 0
                        docker rm %CONTAINER_NAME% || exit 0
                        docker run -d -p 8501:8501 --name %CONTAINER_NAME% %DOCKER_IMAGE%
                    """
                }
            }
        }
    }
}
