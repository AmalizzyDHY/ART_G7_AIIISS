pipeline {
  agent { label 'ai-lab' }
  options {
    timestamps()
    disableConcurrentBuilds()
  }
  triggers { pollSCM('H/2 * * * *') }
  environment {
    LLM_PROVIDER = 'mock'
  }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Install') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          python -m pip install -q -r requirements-dev.txt
          python -m pip install -q --no-deps -e .
        '''
      }
    }
    stage('Test') {
      steps {
        sh '''
          . .venv/bin/activate
          python -m pytest --junitxml=reports/pytest.xml
        '''
      }
      post {
        always { junit 'reports/pytest.xml' }
      }
    }
    stage('Terraform validate') {
      steps {
        sh '''
          terraform -chdir=infra init -backend=false -input=false
          terraform -chdir=infra fmt -check
          terraform -chdir=infra validate
        '''
      }
    }
    stage('Build image') {
      steps {
        script {
          env.GROUP = readFile('group.txt').trim()
          env.IMAGE_TAG = "copilot-${env.GROUP}:${env.BUILD_NUMBER}"
        }
        sh 'docker build -t "$IMAGE_TAG" .'
        sh 'mkdir -p reports && echo "$IMAGE_TAG" > reports/image-tag.txt'
      }
    }
    stage('Smoke test (mock)') {
      steps {
        sh 'python3 scripts/container_smoke.py "$IMAGE_TAG" > reports/smoke.txt && cat reports/smoke.txt'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
    }
  }
}
