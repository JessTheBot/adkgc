#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# TODO: Replace these placeholders with your actual values
export PROJECT_ID="slava-jess-bot"
export LOCATION="us-west1" # e.g., us-west1
export REPOSITORY_NAME="chat-bot"          # The name of your Artifact Registry Docker repository
export IMAGE_NAME="jess"                     # The name for your container image
export IMAGE_TAG="latest"                        # The tag for your container image (e.g., latest, v1.0.0)

# Construct the full image path
# Format: {LOCATION}-docker.pkg.dev/{PROJECT_ID}/{REPOSITORY_NAME}/{IMAGE_NAME}:{IMAGE_TAG}
export FULL_IMAGE_PATH="${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${IMAGE_TAG}"

# --- Script ---

echo "------------------------------------"
echo "Starting Docker build and push..."
echo "------------------------------------"
echo "Project ID:       ${PROJECT_ID}"
echo "Location:         ${LOCATION}"
echo "Repository Name:  ${REPOSITORY_NAME}"
echo "Image Name:       ${IMAGE_NAME}"
echo "Image Tag:        ${IMAGE_TAG}"
echo "Full Image Path:  ${FULL_IMAGE_PATH}"
echo "------------------------------------"

# 1. Configure Docker to use gcloud for Artifact Registry authentication
echo "\nConfiguring Docker authentication for ${LOCATION}-docker.pkg.dev..."
gcloud auth configure-docker ${LOCATION}-docker.pkg.dev

echo "\nDocker authentication configured."
echo "------------------------------------"

# 2. Build the Docker image
#    - Assumes your Dockerfile is in the current directory (.)
#    - Tags the image with the full Artifact Registry path
echo "\nBuilding Docker image: ${FULL_IMAGE_PATH}..."
podman build -t "${FULL_IMAGE_PATH}" .

echo "\nDocker image build complete."
echo "------------------------------------"

# 3. Push the Docker image to Artifact Registry
echo "\nPushing image to Artifact Registry: ${FULL_IMAGE_PATH}..."
podman push "${FULL_IMAGE_PATH}"

echo "\nDocker image push complete."
echo "------------------------------------"
echo "Deployment script finished successfully."
echo "------------------------------------"

