FROM debian:bookworm

WORKDIR /app

ENV TZ="Europe/Berlin"

RUN apt update && \
    apt install -y python3 python3-pip cron locales net-tools procps && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

COPY . .

COPY crontab.txt /opt
RUN crontab /opt/crontab.txt

RUN pip3 install -r requirements.txt --break-system-packages

RUN ["chmod", "+x", "/app/processes.sh"]

HEALTHCHECK CMD echo $(( $(netstat -ltn | grep -c 2413) && ($(ps -ef | grep -c cron) - 1) ))
ENTRYPOINT ["/app/processes.sh"]