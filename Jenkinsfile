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
                        docker stop revenueforecast_container || exit 0
                        docker rm revenueforecast_container || exit 0
                        docker run -d -p 8501:8501 --name revenueforecast_container hariharasudhan313/revenueforecast
                    """
                }
            }
        }

    }
}
