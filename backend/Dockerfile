FROM debian:bookworm

WORKDIR /app

RUN apt update && apt install python3 python3-pip -y

COPY . .

RUN pip3 install -r requirements.txt --break-system-packages

HEALTHCHECK CMD netstat -ltn | grep -c 2413
#RUN    ToDo: register cronjob
ENTRYPOINT ["python3", "server.py"]