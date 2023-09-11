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
to perform a linear regression allowing to This library is packaged in a docker image that exposes 
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
  - File server for the target image
  - etc.
### Wikipedia server
Acts as the data source, data is retrieved using the [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) 

### Docker
Provides the execution environment, namely the container based on Ubuntu-22.04 contains all the required Python end Nvidia components necessary for executing the target image.
The target image:
- Exposes the TCP port 8888
- Maps the host file system from persistency
- Provides access to the  

## Repository content
| File/folder | Description   
|:------------|:--------------|
| Main.ipynb | Jupyter notebook allowing access to the api |
| docker_build.sh | Script wrapping the Docker image creation |
| docker_setup.sh | Script that creates the conteeng of the Docker image | 



