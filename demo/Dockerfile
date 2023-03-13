FROM gradle:6-jdk11 as BASE
WORKDIR /car_sim
COPY car_sim ./
RUN gradle shadowJar -i -s --warning-mode all
RUN java -jar build/libs/avro-payloads-1.0-SNAPSHOT-all.jar 10000 5 && mv testdata.txt car_sensor_sim_1.txt 
RUN java -jar build/libs/avro-payloads-1.0-SNAPSHOT-all.jar 10000 5 && mv testdata.txt car_sensor_sim_2.txt  
RUN java -jar build/libs/avro-payloads-1.0-SNAPSHOT-all.jar 10000 5 && mv testdata.txt car_sensor_sim_3.txt


FROM python:3.11-slim-bullseye as KAFKA_DEMO

WORKDIR /app
# RUN mkdir data
COPY --from=BASE /car_sim/car_sensor_sim_*.txt ./data/
COPY requirements.txt requirements.txt
COPY *.py ./

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt


# CMD [ "uvicorn", "producer:app", "--host", "0.0.0.0", "--port", "80"]