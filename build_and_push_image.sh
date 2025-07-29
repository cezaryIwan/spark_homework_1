#!/bin/bash

set -euo pipefail

if [ $# -ne 1 ]; then
  exit 1
fi

IMAGE_FULL="$1"
IMAGE_NAME=$(basename "$IMAGE_FULL")
ACR_NAME=$(echo "$IMAGE_FULL"| cut -d'.' -f1)

echo "Building Python egg from setup.py"
python3 setup.py bdist_egg

echo "Converting line endings in shell scripts to Unix format"
dos2unix docker/*.sh

echo "Building Docker image: $IMAGE_FULL"
docker build \
  --no-cache \
  -t "$IMAGE_FULL"\
  -f docker/Dockerfile \
  docker/ --build-context extra-source=./

echo "Checking Azure CLI login"
if ! az account show > /dev/null 2>&1; then
  echo "Not logged in to Azure. Logging in"
  az login
else
  echo "Already logged in to Azure."
fi

echo "Checking Azure Container Registry login for: $ACR_NAME"
if ! az acr login --name "$ACR_NAME" > /dev/null 2>&1; then
  echo "Logging in to ACR"
  az acr login --name "$ACR_NAME"
else
  echo "Already logged in to ACR."
fi

echo "Pushing Docker image to ACR: $IMAGE_FULL"
docker push "$IMAGE_FULL"


echo "Deleting old Spark driver pod if exists"
kubectl delete pod spark-driver --ignore-not-found


echo "Submitting Spark job using spark_submit.sh"
./spark_submit.sh "$IMAGE_FULL"

