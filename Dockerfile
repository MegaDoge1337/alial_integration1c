FROM ubuntu:20.04
RUN apt-get update -y && apt-get upgrade -y
RUN apt update -y && apt upgrade -y
RUN apt-get install -y curl libpq-dev python3 python3-pip
COPY . app
RUN python3 --version
RUN pip3 install fastapi uvicorn psycopg2 python-dotenv
# RUN pip3 install fastapi -r app/requirements.txt
EXPOSE 8082
ENTRYPOINT cd app && python3 main.py
