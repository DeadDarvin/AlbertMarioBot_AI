ARG BASE_IMAGE=python:3.11-slim-buster
FROM $BASE_IMAGE


# system update & package install
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# pip & requirements
COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

COPY . .
WORKDIR .
EXPOSE 8080
ENV PYTHONPATH "./"

# Execute
CMD ["python", "web_app_server/main.py"]
