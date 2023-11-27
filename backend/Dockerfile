FROM	alpine:latest

WORKDIR /app

RUN     apk -U upgrade
RUN     apk add python3
RUN     python3 -m ensurepip

COPY    . .

RUN     pip3 install -r requirements.txt

HEALTHCHECK CMD netstat -ltn | grep -c 2413
#RUN    ToDo: register cronjob
ENTRYPOINT ["python3", "server.py"]