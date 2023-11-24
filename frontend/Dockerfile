FROM python:3.9-slim

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./web_service.py /home/web_service.py
COPY ./requirements.txt /home/requirements.txt

RUN pip3 install -r /home/requirements.txt

HEALTHCHECK CMD curl --fail http://localhost:2412/_stcore/health

ENTRYPOINT ["streamlit", "run", "/home/web_service.py", "--server.port=2412", "--server.address=0.0.0.0"]