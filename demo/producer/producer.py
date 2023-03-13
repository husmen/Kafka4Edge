import asyncio
import json
import logging
import os
from datetime import datetime
import socket

import msgpack
import uvicorn
from fastapi import FastAPI, Path
from kafka3 import KafkaProducer
from kafka3.errors import KafkaError
from pydantic import BaseModel
from tqdm import tqdm

FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

app = FastAPI(title="Kafka.Producer.DEMO", description="Kafka Producer DEMO", version="0.0.1")

class CarData(BaseModel):
    timestamp: str = ''
    speed: float
    coolant_temp: float
    intake_air_temp: float
    intake_air_flow_speed: float
    battery_percentage: float
    battery_voltage: float
    current_draw: float
    engine_vibration_amplitude: float
    throttle_pos: float
    tire_pressure11: int
    tire_pressure12: int
    tire_pressure21: int
    tire_pressure22: int
    accelerometer11_value: float
    accelerometer12_value: float
    accelerometer21_value: float
    accelerometer22_value: float
    control_unit_firmware: int
    failure_occurred: bool


running_flags: list[bool] = []
dataset : list[list[list[CarData]]] = []

def on_send_success(record_metadata):
    # Successful result returns assigned partition and offset
    logging.info(f"MESSAGE SENT: {record_metadata.topic} {record_metadata.partition} {record_metadata.offset}")

def on_send_error(excp):
    logging.error('MESSAGE ERROR: ', exc_info=excp)
    # handle exception

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

async def produce_data(node_id: int, car_id: int, data_point_count: int, data_point_interval: int):
    global dataset

    try:
        # configure broker and serializer, msgpack provides better performance than json
        producer = KafkaProducer(bootstrap_servers=['kafka-0:9092', 'kafka-1:9092', 'kafka-2:9092'], 
                                client_id=f'{socket.gethostname()}_{node_id}', 
                                value_serializer=msgpack.dumps, 
                                acks=1, # default 1
                                compression_type='lz4', 
                                retries=1,
                                batch_size=16384 # default 16KB
                                )

        for data_point in dataset[node_id][car_id][:data_point_count]:
            # Asynchronous by default
            data_point.timestamp = datetime.now().isoformat()
            producer.send('car_data', {f'car_{node_id}{car_id}': data_point.dict()}).add_callback(on_send_success).add_errback(on_send_error)
            await asyncio.sleep(data_point_interval / 1000)
    except Exception as ex:
        logging.error('PRODUCE TASK ERROR: ', exc_info=ex)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.put("/kafka/start/{node_id}/{car_count}/{data_point_count}/{data_point_interval}")
async def kafka_root(node_id: int = Path(example=0, description='Node ID'), car_count: int = Path(example=5, description='Number of cars'), data_point_count: int = Path(example=10000, description='Number of data points'), data_point_interval: int = Path(example=100, description='Interval between data points in ms')):
    if running_flags[node_id]:
        return {"Tasks": "Already Running"}
    
    running_flags[node_id] = True
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(produce_data(node_id, car_id, data_point_count, data_point_interval)) for car_id in range(0, car_count)]
        while not all([t.done() for t in tasks]):
            await asyncio.sleep(3)
            if not running_flags[node_id]:
                _ = [t.cancel() for t in tasks]
                break

    return {"Tasks": "Started"}


@app.put("/kafka/stop/{node_id}")
async def kafka_root(node_id: int = Path(example=0, description='Node ID')):
    global running_flags

    if running_flags[node_id]:
        running_flags[node_id] = False
    
    return {"Tasks": "Stopped"}


async def load_data():
    global dataset
    global running_flags
    logging.info('## Loading simulated car sensor data...')

    for (root, dirs, files) in os.walk('data'):
        for fn in files:
            if fn.endswith('.txt'):
                fp = os.path.join(root, fn)
                with open(fp, 'r') as f:
                    sensor_data = f.readlines()

                data_points = [None] * len(sensor_data)
                for i in tqdm(range(len(sensor_data))):
                    data_points[i] = CarData(**json.loads(sensor_data[i]))

                # data_points = [CarData(**json.loads(data_raw)) for data_raw in sensor_data]
                
                car_data = [data_points[i:i + 10000] for i in range(0, len(data_points), 10000)]
                dataset.append(car_data)
                running_flags.append(False)
                

def test_kafka():
    logging.info("# Kafka producer test")
    hosts = ['localhost:9092', '127.0.0.1:9092', 'http://127.0.0.1:9092', 'kafka-0:9092', 'http://kafka-0:9092']

    for host in hosts:
        try:
            producer = KafkaProducer(bootstrap_servers=[host], client_id='test', value_serializer=msgpack.dumps)
            logging.info(f"## Kafka broker {host} is available")
            try:
                producer.send('test', {'test': 'test'}).add_callback(on_send_success).add_errback(on_send_error)
                logging.info(f"## Kafka broker {host} is working")
            except Exception as ex:
                logging.error('## Kafka produce ERROR: ', exc_info=ex)

            producer.close()
        except Exception as ex:
            logging.error(f"## Kafka broker {host} is not available", exc_info=ex)


if __name__ == "__main__":
    logging.info("# Kafka producer demo started")
    asyncio.run(load_data()) 

    test_kafka()

    kwargs = {"host": "0.0.0.0", "port": 80}  # do not use Debug in production
    uvicorn.run(app, **kwargs)