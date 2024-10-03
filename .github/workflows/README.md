# CI/CD Pipeline for Notejam Flask Application

This repository contains a GitHub Actions workflow that implements a Continuous Integration and Continuous Deployment (CI/CD) pipeline for a Notejam Flask application. The pipeline automates the process of building a Docker image, pushing it to Amazon Elastic Container Registry (ECR), and deploying it to Amazon Elastic Container Service (ECS).

## Workflow Overview

The workflow consists of two main jobs: `build` and `deploy`. Additional jobs and steps for multi-environment deployments, linting, security scanning, notifications, and rollback are included but commented out for future use.

### Build Job

The build job performs the following steps:

1. Checks out the repository
2. Sets up Python (for potential future use)
3. Installs dependencies (for potential future use)
4. Sets up Docker Buildx
5. Configures AWS credentials
6. Logs in to Amazon ECR
7. Creates an ECR repository if it doesn't exist
8. Builds the Docker image
9. Pushes the Docker image to ECR

### Deploy Job

The deploy job runs after the build job completes and performs these steps:

1. Checks out the repository
2. Configures AWS credentials
3. Downloads the ECS task definition
4. Deploys the updated task definition to ECS
5. Verifies the ECS service health

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

## Usage

This workflow is triggered on two events:
1. Push to the `main` branch
2. Pull request to the `main` branch

When triggered, it will automatically build, push, and deploy your application.

## Customization

You may need to customize the workflow based on your specific requirements:

1. Modify the `branches` in the trigger section if you use a different branch naming convention.
2. Adjust the `aws-region` if your resources are in a different AWS region.
3. Update the `container-name` in the deploy job if your task definition uses a different container name.
4. Modify the Dockerfile in your repository to match your application's build process.

## Future Enhancements

The workflow includes commented-out sections for the following features:

1. Linting: A step to run flake8 for code style checking.
2. Security Scanning: A step to use Snyk for vulnerability scanning.
3. Multi-environment Deployments: Logic to deploy to different environments based on the branch.
4. Notifications: Steps to send Slack notifications for successful deployments and rollbacks.
5. Rollback Mechanism: A job to automatically roll back to the previous version if the deployment fails.

To enable these features in the future:

1. Uncomment the relevant sections in the workflow file.
2. Configure any necessary additional secrets (e.g., `SNYK_TOKEN`, `SLACK_WEBHOOK`).
3. Set up the required resources (e.g., separate ECS clusters for different environments).
4. Update the workflow file with the correct resource names and configurations.

## Troubleshooting

The workflow includes several debug steps to help with troubleshooting:

1. Printing AWS environment variables
2. Debugging Task Definition ARN
3. Printing ECS cluster and service names

Check the workflow run logs in GitHub Actions for these debug outputs if you encounter any issues.

## Security Note

Ensure that your AWS credentials are stored securely as GitHub secrets and that the IAM user or role associated with these credentials follows the principle of least privilege.
