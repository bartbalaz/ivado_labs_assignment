# IVADO LABS Assignment

# Requirements

## Description
A new world organization has just been created. It includes all the museum management committees that have more than 2,000,000 visitors annually. This list is available via __[Wikipedia](https://en.wikipedia.org/wiki/List_of_most_visited_museums)__
This new organization wishes to correlate the tourist attendance at their museums with the population of the respective cities. To achieve this, a small, common and harmonized database must be built to be able to extract features. This DB must include the characteristics of museums as well as the population of the cities in which they are located. You have been chosen to build this database. In addition, you are asked to create a small linear regression ML algorithm to correlate the city population and the influx of visitors.  Your solution must balance the need for quickly assessing the data, rapid prototyping and deploying a MVP to a (potentially) public user that could later scale. You must use the Wikipedia APIs to retrieve this list of museums and their characteristics. You are free to choose the source of your choice for the population of the cities concerned.

## Deliverables
- It is required that your code is a structured Python project. The code should be packaged and exposed in a Docker container (use Docker Compose if you require additional infrastructure).
- A jupyter notebook hosted in docker should also be created. This notebook should  programmatically use your other code to visually present the results of your regression model.

## Notes
You will be evaluated not only on how your code works but also on the rationale for the choices you make. you make.

# Solution

## General idea
As per requirements a small library is developed. The library allows to gather and prepare the required data for further analysis. The analysis consists in training an ML model 
to perform a linear regression allowing to predict the museum visits based on the size of the city the museum is located in. This library is packaged in a docker image that exposes 
a Jupyter notebook. The notebook allows to invoke the different functions from the library.   

## High level deployment layout
The figure below depicts the deployment layout.

![Deployment layout](docs/layout.jpg)

### Host
Has the following purposes:
- **Development platform**: While developing the solution a Linux Ubuntu-22.04 (WSL) is used as the development platform. 
It hosts the IDE along with all the necessary environment, tools and libraries for image creation, easy execution and testing  
- **Execution platform** for the target image:
  - GPUs
  - Docker server
  - Docker registry
  - File server for Docker image persistency
  
### Wikipedia server
Acts as the data source, data is retrieved using the [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) 

### Docker
Provides the execution environment, namely the container based on Ubuntu-22.04 contains all the required Python end Nvidia components necessary for executing the target image.
The target image:
- Exposes the TCP port 8888
- Maps the host file system for persistency, Docke image internal __/run__ folder to __<cloned directory>__
- Provides access to the GPU hardware

## Repository content
|    File/folder    |   Type    | Description                                          |                                          
|:-----------------:|:---------:|:-----------------------------------------------------|
|    Main.ipynb     |   File    | Jupyter notebook allowing access to the api          |
|  docker_build.sh  |   File    | Script wrapping the Docker image creation            |
|  docker_setup.sh  |   File    | Script that creates the conteeng of the Docker image |
|  docker_start.sh  |   File    | Script wrapping the docker container startup         |
|    Dockerfile     |   File    | Docker image description file                        | 
| requirements.txtt |   File    | Python dependencies requirements                     |
|     start.sh      |   File    | Jupyter notebook startup script, command line for development purpose or Docker image entry point | 
|      test.sh      |   File    | Scrpt launching the unit tests |
|  jupyter_config   | Directory | Contains the Jupyter notebook configuraiton |
|       data        | Directory | Contains the saved master data and regression trained model |
|        src        | Directory | Contains the main library source code |
|       test        | Directory | Contains the main library test scripts| 

## Limitations
This is a demo/assignment application, because of time constrainte it contains the following constraints:
- The security considerations have been omitted: It is possible to inject malicious values through the API
- Model persistency is achieved using Python **pickle** library which is not secure
- The system has neither been designed nor tested for all the possible corner cases
- The unit test set only contains several test cases.
- Comments are minimal
- Only the Ubuntu-22.04 on Windows 11 WSL2 with Nvidia GPU support configuration has been tested, other configuration will require deployment adjustments

## Source code structure
- __src/museums.py__: Contains the main api module that allows to access all the feature of the application
- __src/components/data.py__: Contains the implementation of the data extraction and basic data preparation functionalities including the persistancy
- __src/components/model.py__: Contains the implementation of the linear regression model

## Prerequisites
- Intel 64bit platform
- Windows 11 host
- Ubuntu-22.04 in the Windows 11 WSL2 environment
- Docker service
- Python 3.10.x
- Pip 22.x.y
- Optional Nvidia GPU graphic card
- Optionally Nvidia prerequisites, setup procedure may be found [here](https://developer.nvidia.com/cuda-downloads) 
- Optionally Nvidia docker support procedure may be found [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Workflows
### Development
- Clone the [repository](https://github.com/bartbalaz/ivado_labs_assignment) to __assignment__ folder
```commandline
git clone git@github.com:bartbalaz/ivado_labs_assignment.git assignemnt
```
- Switch to the cloned repository
```commandline
cd assignment
```
- Optionl: Run the unit tests
```commandline
./test.sh
```
- Optional: Start Jupyter notebook locally
```commandline
./start.sh
```
- Buld the Docker image
```commandline
./docker_build.sh
```
- Start the docker image
```commandline
./docker_start.sh
```


