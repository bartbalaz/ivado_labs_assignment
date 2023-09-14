#!/bin/bash

IMAGE_NAME=ivado_labs_assignment

# If the docker is started in isolation mode no folders are mounted and the container is kept (i.e. no "--rm" option)
# after finishing the execution
if [ "$1" == "--isolation" ] || [ "$1" == "-i" ]; then
    # See if a container has already been crated in the past
    CONTAINER_ID=$(docker container ps -a --filter "ancestor=$IMAGE_NAME" --filter "status=exited" -q)
    if [ ! -z "$CONTAINER_ID" ]; then
      # if yes then reuse it
      echo "Resuming container $CONTAINER_ID"
      docker start $CONTAINER_ID && docker attach $CONTAINER_ID
    else
      # if not, spin a new container
      echo "Starting a new container from image $IMAGE_NAME"
      docker run -it -p 8888:8888 --gpus=all $IMAGE_NAME
    fi
else
    docker run --rm -it -p 8888:8888 --gpus=all -v $(pwd):/run ivado_labs_assignment
fi

