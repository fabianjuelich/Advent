FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

HEALTHCHECK CMD curl -k --fail https://localhost:2412/_stcore/health

ENTRYPOINT ["streamlit", "run", "web_service.py", "--server.port=2412", "--server.address=0.0.0.0"]
