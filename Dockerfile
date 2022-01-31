FROM python:3.10

WORKDIR /notebook
COPY . .
RUN pip install -r requirements.txt