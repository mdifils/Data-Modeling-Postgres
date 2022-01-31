FROM python:3.10

# /notebook folder will be created and set as working directory
WORKDIR /notebook
# copy all files in the current directory (except those mentioned in dockerignore)
# to the working directory in the container
COPY . .
# installing all dependancies packages in the container
RUN pip install -r requirements.txt