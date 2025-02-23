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
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
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
