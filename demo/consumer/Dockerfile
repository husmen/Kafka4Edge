FROM python:3.11-slim-bullseye as kafka_demo
WORKDIR /app
COPY ./demo/requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

FROM kafka_demo
WORKDIR /app
COPY ./demo/consumer/*.py ./

# CMD [ "python", "consumer.py"]