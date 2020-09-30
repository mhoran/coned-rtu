FROM python:alpine@sha256:bcca0a38a207b7b40c46e059e6ecf1ba3af833be665fb65ab8b7e81ac601e7d3

WORKDIR /root

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY coned.py .
COPY reading.py .
ENTRYPOINT ["python3", "main.py"]
