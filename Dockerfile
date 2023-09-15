FROM ubuntu:22.04

EXPOSE 8888/tcp

# Create a run directory and copy the setup script into it
ADD docker_setup.sh requirements.txt start.sh Main.ipynb /run/
ADD src /run/src/
ADD data /run/data

RUN /run/docker_setup.sh

# Start (only possible after mounting the run folder)
ENTRYPOINT /run/start.sh /run