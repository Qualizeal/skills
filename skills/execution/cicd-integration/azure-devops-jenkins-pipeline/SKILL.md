---
name: azure-devops-jenkins-pipeline
description: "Working Azure DevOps and Jenkins configurations for sharded test execution with result publishing and credential handling. Use when configuring tests on Azure DevOps or Jenkins."
---

# Azure DevOps and Jenkins pipelines

## Azure DevOps

```yaml
trigger: [main]

pool:
  vmImage: ubuntu-latest

jobs:
  - job: e2e
    timeoutInMinutes: 30
    strategy:
      parallel: 4
    steps:
      - task: NodeTool@0
        inputs: { versionSpec: '20.x' }
      - script: npm ci && npx playwright install --with-deps
      - script: npx playwright test --shard=$(System.JobPositionInPhase)/$(System.TotalJobsInPhase)
        env:
          TEST_USER_PASSWORD: $(TEST_USER_PASSWORD)
      - task: PublishTestResults@2
        condition: succeededOrFailed()
        inputs:
          testResultsFormat: JUnit
          testResultsFiles: 'results/junit.xml'
          mergeTestResults: true
```

Use templates for shared stages, and set `timeoutInMinutes` on every job.

## Jenkins

```groovy
pipeline {
  agent { docker { image 'mcr.microsoft.com/playwright:v1.50.0-noble' } }
  options { timeout(time: 30, unit: 'MINUTES'); disableConcurrentBuilds() }
  stages {
    stage('E2E') {
      steps {
        sh 'npm ci'
        withCredentials([string(credentialsId: 'test-user-password', variable: 'TEST_USER_PASSWORD')]) {
          sh 'npx playwright test --grep @p0'
        }
      }
    }
  }
  post {
    always {
      junit 'results/junit.xml'
      archiveArtifacts artifacts: 'playwright-report/**', allowEmptyArchive: true
    }
  }
}
```

Declarative pipelines with a shared library; avoid inline scripts that cannot be reviewed as code.
