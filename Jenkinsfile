pipeline {
    agent any
    environment {
        GITHUB_REPO_URL = 'https://github.com/Sengar001/CVSS_Score_Predictor.git'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${GITHUB_REPO_URL}"
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Training') {
            steps {
                sh 'python scripts/train.py'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t cvss-score-predictor:latest .'
            }
        }
        // stage('Push to DockerHub') {
        //     steps {
        //         withCredentials([string(credentialsId: 'dockerhub-pass', variable: 'DOCKER_PASSWORD')]) {
        //             sh '''
        //                 echo $DOCKER_PASSWORD | docker login -u your_dockerhub_username --password-stdin
        //                 docker tag cvss-mlops:latest your_dockerhub_username/cvss-mlops:latest
        //                 docker push your_dockerhub_username/cvss-mlops:latest
        //             '''
        //         }
        //     }
        // }
    }
}
