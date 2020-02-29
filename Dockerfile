FROM selenium/standalone-chrome

USER root
RUN apt-get update && apt-get upgrade -yq
RUN apt-get install python3 python3-pip -y
USER seluser

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY coned.py .
COPY reading.py .
ENTRYPOINT ["python3", "main.py"]
