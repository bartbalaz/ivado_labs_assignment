echo "Starting environment"

export JUPYTER_CONFIG_DIR="./jupyter_config"

# This should only happen once
if [ ! -d "$JUPYTER_CONFIG_DIR" ]; then
  echo "Creating jupyter configuration directory!!!"
  mkdir $JUPYTER_CONFIG_DIR
  jupyter lab  --generate-config
fi

# Make sure jupyter does not wander anywhere else in the os
export JUPYTER_CONFIG_PATH=""

export JUPYTER_RUNTIME_DIR="./.jupyter_runtime"

# This should happen everytime the container is started
if [ ! -d "$JUPYTER_RUNTIME_DIR" ]; then
  mkdir $JUPYTER_RUNTIME_DIR
fi

jupyter lab --no-browser --ip='*' --NotebookApp.token='' --NotebookApp.password=''