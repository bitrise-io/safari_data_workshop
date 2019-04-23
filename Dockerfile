# use official Python runtime as a parent image 
# https://hub.docker.com/_/python/
FROM python:latest 

# set working directory 
WORKDIR /safari_workshop 

# copy current directory contents to container at safari_workshop 
ADD . /safari_workshop

# install any needed packaged specified in requirements.txt 
RUN pip install --requirement requirements.txt --upgrade

# make port available to the world ourside this computer 
EXPOSE 90

# build image
# docker build . -t safari_workshop_image

# attach current folder and make it the working directory
# docker run -it --rm --name <NAME OF CONTAINER> -v <LOCAL FOLDER>:<DOCKER FOLDER> -w <WORKDIR ON DOCKER> <IMAGE>:<VERSION> <COMMAND>

# linux / unix
# docker run --rm --name safari_workshop_container -v "$PWD":/safari_workshop_folder -w /safari_workshop_folder safari_workshop_image:latest python load_data.py

# windows
# not working when there is a spane in the path
# docker run --rm --name safari_workshop_container -v ${pwd}:/safari_workshop_folder -w /safari_workshop_folder safari_workshop_image:latest python load_data.py