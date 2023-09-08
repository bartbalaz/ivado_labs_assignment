echo "Starting environment"
echo

# Project configuration
export WORK_DIR=$(pwd)
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src

# Jupyter configuraiton
export JUPYTER_CONFIG_DIR=$WORK_DIR/jupyter_config
export JUPYTER_CONFIG_PATH=""
export JUPYTER_RUNTIME_DIR=$WORK_DIR/.jupyter_runtime

echo "Configuration"
echo "------------"
echo WORK_DIR: "$WORK_DIR"
echo PYTHONPATH: "$PYTHONPATH"
echo JUPYTER_CONFIG_DIR: "$JUPYTER_CONFIG_DIR"
echo JUPYTER_CONFIG_PATH: "$JUPYTER_CONFIG_PATH"
echo JUPYTER_RUNTIME_DIR: "$JUPYTER_RUNTIME_DIR"

if [ ! -d "$JUPYTER_CONFIG_DIR" ] && [ "$MODE" == "dev" ]; then
  echo "Creating jupyter configuration directory"
  mkdir $JUPYTER_CONFIG_DIR
  jupyter lab  --generate-config
fi

jupyter lab --no-browser --ip='*' --NotebookApp.token='' --NotebookApp.password=''