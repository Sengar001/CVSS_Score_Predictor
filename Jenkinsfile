pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sengar001/cvss-mlops:latest'
        GITHUB_REPO_URL = 'https://github.com/Sengar001/CVSS_Score_Predictor.git'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${GITHUB_REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Push Docker Image') {
        steps {
            withCredentials([usernamePassword(credentialsId: 'DockerHubCred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                script {
                    def loginStatus = sh(script: 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin', returnStatus: true)
                    if (loginStatus != 0) {
                        error("Docker login failed. Check credentials and try again.")
                    }

                    def pushStatus = sh(script: 'docker push $DOCKER_IMAGE', returnStatus: true)
                    if (pushStatus != 0) {
                        error("Docker image push failed. Check DockerHub repository permissions.")
                    }
                }
        }
    }
}

        // stage('Push to DockerHub') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
        //             sh """
        //                 echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
        //                 docker push ${DOCKER_IMAGE}:latest
        //             """
        //         }
        //     }
        // }

        // stage('Deploy Container') {
        //     steps {
        //         sh "docker run -d -p 8000:8000 --name cvss-app ${DOCKER_IMAGE}:latest"
        //     }
        // }
    }
}
