FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install ipmitool -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-u", "controller.py"]
