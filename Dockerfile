FROM selenium/standalone-chrome@sha256:56384f50933cc85ded9e671df4817934b9b7c2df7ef2cd302b1fe1a4ccaa80a8

USER root
RUN apt-get update && apt-get upgrade -yq
RUN apt-get install python3 python3-pip -y
USER seluser

WORKDIR /home/seluser/coned-rtu

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY coned.py .
COPY reading.py .
ENTRYPOINT ["python3", "main.py"]
