#!/bin/bash
# This script builds and pushes a Docker image to GitHub Container Registry (ghcr.io)
# Prerequisites:
# 1. You need to create a Personal Access Token (PAT) with 'write:packages' scope
#    at https://github.com/settings/tokens
# 2. Export your GitHub username and PAT as environment variables:
#    export GITHUB_USERNAME=your-username
#    export GITHUB_TOKEN=your-personal-access-token
#
# Alternatively, you can pass them as arguments:
# ./push.sh <github_username> <github_token>

# Get GitHub credentials either from arguments or environment variables
GITHUB_USERNAME=${1:-$GITHUB_USERNAME}
GITHUB_TOKEN=${2:-$GITHUB_TOKEN}

# Check if credentials are provided
if [ -z "$GITHUB_USERNAME" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GitHub username and token are required."
    echo "Usage: ./push.sh <github_username> <github_token>"
    echo "Or set environment variables GITHUB_USERNAME and GITHUB_TOKEN"
    exit 1
fi

# Login to GitHub Container Registry
echo "Logging in to GitHub Container Registry..."
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin

# Build the Docker image
echo "Building Docker image..."

docker buildx create --use  # Enable buildx
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/tschm/cradle:latest --push .

#docker build -t ghcr.io/tschm/cradle:latest .

# Push the Docker image
# echo "Pushing Docker image to ghcr.io..."
# docker push ghcr.io/tschm/cradle:latest

# Logout for security
echo "Logging out from GitHub Container Registry..."
docker logout ghcr.io

echo "Done!"
