FROM	alpine:latest

RUN     apk -U upgrade
RUN     apk add python3
RUN     python3 -m ensurepip

COPY    ./requirements.txt  /home/requirements.txt
RUN     pip3 install -r /home/requirements.txt

COPY    ./server    /home/server
COPY    ./cronjob   /home/cronjob