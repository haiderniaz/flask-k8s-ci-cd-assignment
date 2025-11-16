pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo '========================================'
                    echo 'Stage 1: Building Docker Image'
                    echo '========================================'
                    sh 'docker build -t flask-app:latest .'
                    echo 'Docker image built successfully: flask-app:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo '========================================'
                    echo 'Stage 2: Deploying to Kubernetes'
                    echo '========================================'
                    sh 'kubectl apply -f kubernetes/'
                    echo 'Kubernetes manifests applied successfully'
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    echo '========================================'
                    echo 'Stage 3: Verifying Deployment'
                    echo '========================================'
                    echo 'Checking rollout status...'
                    sh 'kubectl rollout status deployment/flask-app --timeout=5m'
                    echo ''
                    echo 'Verifying pods...'
                    sh 'kubectl get pods -l app=flask-app'
                    echo ''
                    echo 'Verifying services...'
                    sh 'kubectl get services -l app=flask-app'
                    echo ''
                    echo 'Checking deployment status...'
                    sh 'kubectl get deployments flask-app'
                    echo ''
                    echo 'All verification checks passed!'
                }
            }
        }
    }

    post {
        success {
            echo '========================================'
            echo 'Pipeline completed successfully!'
            echo '========================================'
        }
        failure {
            echo '========================================'
            echo 'Pipeline failed!'
            echo '========================================'
        }
    }
}


