echo "Starting environment"
echo

# either dev of prod
if [ -z "$MODE" ]; then
  export MODE=dev
fi

if [ "$MODE" == "dev" ]; then
  export WORK_DIR=$(pwd)
else
  export WORK_DIR=$(pwd)/work
fi

export REPO_DIR=$(pwd)/repo
export WORKBOOK=$WORK_DIR/Main.ipynb
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src
export JUPYTER_CONFIG_DIR=$(pwd)/jupyter_config
export JUPYTER_CONFIG_PATH=""
export JUPYTER_RUNTIME_DIR=$WORK_DIR/.jupyter_runtime

echo "Configuration"
echo "------------"
echo MODE: "$MODE"
echo WORK_DIR: "$WORK_DIR"
echo REPO_DIR: "$REPO_DIR"
echo WORKBOOK: "$WORKBOOK"
echo PYTHONPATH: "$PYTHONPATH"
echo JUPYTER_CONFIG_DIR: "$JUPYTER_CONFIG_DIR"
echo JUPYTER_CONFIG_PATH: "$JUPYTER_CONFIG_PATH"
echo JUPYTER_RUNTIME_DIR: "$JUPYTER_RUNTIME_DIR"

if [ ! -d "$REPO_DIR" ]; then
  echo "Creating REPO_DIR: $REPO_DIR"
  mkdir $REPO_DIR
fi

if [ ! -d "$WORK_DIR" ]; then
  echo "Creating work directory"
  mkdir $WORK_DIR
fi

if [ ! -d "$JUPYTER_CONFIG_DIR" ] && [ "$MODE" == "dev" ]; then
  echo "Creating jupyter configuration directory"
  mkdir $JUPYTER_CONFIG_DIR
  jupyter lab  --generate-config
fi

# This should happen everytime the container is started
if [ ! -d "$JUPYTER_RUNTIME_DIR" ]; then
  echo "Creating jupyter runtime directory"
  mkdir $JUPYTER_RUNTIME_DIR
fi

if [ "$MODE" != "dev" ] && [ ! -f "$WORKBOOK" ]; then
    cp Main.ipynb "$WORKBOOK"
    cd $WORK_DIR
fi

jupyter lab --no-browser --ip='*' --NotebookApp.token='' --NotebookApp.password=''