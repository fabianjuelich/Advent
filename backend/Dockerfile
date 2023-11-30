FROM debian:bookworm

WORKDIR /app

ENV TZ="Europe/Berlin"

RUN apt update && \
    apt install -y python3 python3-pip locales net-tools && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

COPY . .

RUN pip3 install -r requirements.txt --break-system-packages

HEALTHCHECK CMD netstat -ltn | grep -c 2413
#RUN    ToDo: register cronjob
ENTRYPOINT ["python3", "server.py"]