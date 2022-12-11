FROM python:3.8

RUN apt update && apt install -y gcc python3-dev musl-dev

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
COPY ./infrastructure/config.deploy.yaml ./config.yaml
WORKDIR .
CMD ["python", "main.py"]