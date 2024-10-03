# CI/CD Pipeline for Notejam Flask Application

This repository contains a GitHub Actions workflow that implements a Continuous Integration and Continuous Deployment (CI/CD) pipeline for a Notejam Flask application. The pipeline automates the process of building a Docker image, pushing it to Amazon Elastic Container Registry (ECR), and deploying it to Amazon Elastic Container Service (ECS).

## Workflow Overview

The workflow now consists of three main jobs: `build`, `deploy`, and `rollback` (commented out by default).

### Build Job

The build job performs the following steps:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Runs linting (commented out)
5. Runs security scanning (commented out)
6. Sets up Docker Buildx
7. Configures AWS credentials
8. Logs in to Amazon ECR
9. Creates an ECR repository if it doesn't exist
10. Builds the Docker image
11. Pushes the Docker image to ECR

### Deploy Job

The deploy job runs after the build job completes and performs these steps:

1. Checks out the repository
2. Configures AWS credentials
3. Downloads the ECS task definition
4. Deploys the updated task definition to ECS
5. Verifies the ECS service health
6. Sends a notification (commented out)

### Rollback Job (Commented Out)

The rollback job is designed to revert to the previous version if the deployment fails:

1. Configures AWS credentials
2. Rolls back to the previous task definition
3. Sends a notification

## Prerequisites

Before using this workflow, ensure you have the following:

1. An AWS account with appropriate permissions
2. An ECS cluster and service set up
3. An ECR repository (the workflow can create this if it doesn't exist)
4. The following secrets configured in your GitHub repository:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `AWS_ACCOUNT_ID`
   - `ECR_REPOSITORY`
   - `DOCKER_IMAGE_NAME`
   - `ECS_CLUSTER`
   - `ECS_SERVICE`
   - `SLACK_WEBHOOK` (for notifications, if enabled)

## Usage

This workflow is triggered on three events:
1. Push to the `main` branch (deploys to production)
2. Push to the `develop` branch (deploys to staging)
3. Pull request to the `main` or `develop` branch

When triggered, it will automatically build, push, and deploy your application to the appropriate environment.

## Customization

You may need to customize the workflow based on your specific requirements:

1. Modify the `branches` in the trigger section if you use a different branch naming convention.
2. Adjust the `aws-region` if your resources are in a different AWS region.
3. Update the `container-name` in the deploy job if your task definition uses a different container name.
4. Modify the Dockerfile in your repository to match your application's build process.
5. Uncomment and configure the linting step if you want to include code style checks.
6. Uncomment and configure the security scanning step to check for vulnerabilities.
7. Uncomment and configure the notification steps if you want to receive Slack notifications.
8. Uncomment and configure the rollback job if you want automatic rollbacks on failure.

## Environment-Specific Deployments

The workflow now supports deploying to different environments based on the branch:

- Pushes to `main` deploy to the production environment
- Pushes to `develop` deploy to the staging environment

Ensure you have the appropriate ECS clusters and services set up for each environment.

## Linting (Commented Out)

The workflow includes a commented-out step for linting using flake8. Uncomment and adjust this step to enforce your project's code style guidelines.

## Security Scanning (Commented Out)

A security scanning step using Snyk is included but commented out. Uncomment and configure this step to check for vulnerabilities in your dependencies and Docker image.

## Rollback Mechanism (Commented Out)

A rollback job is included but commented out. This job can automatically revert to the previous version if the deployment fails. Uncomment and configure this job if you want to enable automatic rollbacks.

## Notifications (Commented Out)

The workflow includes commented-out steps to send Slack notifications for successful and failed deployments. Uncomment and configure these steps if you want to receive notifications.

## Troubleshooting

The workflow includes several debug steps to help with troubleshooting:

1. Printing AWS environment variables
2. Debugging Task Definition ARN
3. Printing ECS cluster and service names

Check the workflow run logs in GitHub Actions for these debug outputs if you encounter any issues.

## Security Note

Ensure that your AWS credentials are stored securely as GitHub secrets and that the IAM user or role associated with these credentials follows the principle of least privilege.
