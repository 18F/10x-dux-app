#!/bin/bash
# A script to start a Docker image, passing existing AWS credentials, and pass a command to the image

# Obtain the directory of the script
SCRIPT_DIR=$(pwd)

DOCKER_ENV=""
for VAR in $(printenv | egrep -e '^INPUT_'); do
  echo "Addinng ${VAR}"
  DOCKER_ENV="-e ${VAR} ${DOCKER_ENV}"
done

echo "Shell out to the provision docker container" 
docker run -it ${DOCKER_ENV} -v "$(pwd):/app" -w /app --entrypoint /bin/bash cg-cli-tools "$@"
