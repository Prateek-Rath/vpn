pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "pratster20"       // need to replace
        APP_IMAGE = "${DOCKER_REGISTRY}/spe-app:latest"
        VPN_IMAGE = "${DOCKER_REGISTRY}/spe-vpn:latest"
        DOCKER_CREDENTIALS_ID = "dockerhub-creds" // need to add in jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                        sh "docker build -t ${APP_IMAGE} ./app"
                        sh "docker build -t ${VPN_IMAGE} ./vpn"
                        sh "docker push ${APP_IMAGE}"
                        sh "docker push ${VPN_IMAGE}"
                    }
                }
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                sh "ansible-playbook -i ./ansible/inventory.ini ./ansible/playbook.yml --vault-password-file password.txt"
            }
        }
    }
}
