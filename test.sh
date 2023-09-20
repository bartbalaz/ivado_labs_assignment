#!/bin/bash

export TEST_PATH_ROOT=$(pwd)

python  -m unittest discover -q -s ./test