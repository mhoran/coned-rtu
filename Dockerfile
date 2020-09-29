FROM python:alpine@sha256:9eb16c4046fa7e9ac838563fd3b7a0e006142bb6ac944199eda5a0fa60a9cf02

WORKDIR /root

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY coned.py .
COPY reading.py .
ENTRYPOINT ["python3", "main.py"]
