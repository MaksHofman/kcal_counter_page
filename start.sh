#!/usr/bin/env bash

if [ "$1" = -h ]; then
  echo "Usage: $0 [clean]"
  exit 1
fi

sudo ss -lptn 'sport = :8080' | kill $(awk '{print $6}' | cut -d, -f1 | cut -d= -f2)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "${PROJECT_DIR}")"

# stop previous running containers
if [ -n "$(docker ps -a | grep "${PROJECT_NAME}")" ]; then
  docker ps -a | grep "${PROJECT_NAME}" | awk '{print $1}' | xargs docker stop
fi

# remove previous containers
if [ -n "$(docker ps -a | grep "${PROJECT_NAME}")" ] && [ "$1" == "clean" ]; then
  docker ps -a | grep "${PROJECT_NAME}" | awk '{print $1}' | xargs docker rm
  docker image ls | grep "${PROJECT_NAME}" | awk '{print $3}' | xargs docker rmi
fi

set -euo pipefail

# check is there a docker-compose command, if not, use "docker compose" instead.
if [ -x "$(command -v docker-compose)" ]; then
    dc=docker-compose
else
    dc="docker compose"
fi

export website_IMAGE_NAME="${PROJECT_NAME}-flask"
export website_PROJ_DIR="${PROJECT_DIR}/site"
export website_COMPOSE_FILE="${website_PROJ_DIR}/docker-compose.yml"

if [ ! -n "$(docker image ls | grep "${PROJECT_NAME}-flask")" ]; then
  docker build -t "${PROJECT_NAME}-flask" "${website_PROJ_DIR}"
  export website_IMAGE_NAME="${PROJECT_NAME}-flask"
fi

${dc} -p "${PROJECT_NAME}" -f "${website_COMPOSE_FILE}" up -d 

export db_PROJ_DIR="${PROJECT_DIR}/postgres"
export db_COMPOSE_FILE="${db_PROJ_DIR}/docker-compose.yml"

${dc} -p "${PROJECT_NAME}" -f "${db_COMPOSE_FILE}" up -d 
