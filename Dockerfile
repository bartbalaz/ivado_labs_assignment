FROM ubuntu:22.04

# Exposing the Jupyter default port
EXPOSE 8888/tcp

# Create a run directory and copy the required files for setting up the image
ADD docker_setup.sh requirements.txt start.sh Main.ipynb /run/
# Add the python libraries
ADD src /run/src/
# Add the existing data files
ADD data /run/data

# Configure the image
RUN /run/docker_setup.sh

# Jupyter notebook start script
ENTRYPOINT /run/start.sh /run