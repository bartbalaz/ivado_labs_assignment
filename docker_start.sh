#!/bin/bash

docker run --rm -it -p 8888:8888 --gpus=all -v $(pwd):/run challenge