import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
import socket

import msgpack
import uvicorn
from fastapi import FastAPI, Path
from kafka3 import KafkaConsumer
from kafka3.errors import KafkaError
from pydantic import BaseModel
from tqdm import tqdm

FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

sizes = []
latencies = []
timestamps = []

async def consume_data(consumer):
    global sizes, latencies, timestamps

    for msg in consumer:
        timestamps.append(datetime.now())
        msg_keys = [k for k in msg.value.keys()]
        send_timestamp = msg.value[msg_keys[0]]['timestamp']
        sizes.append(msg.value.__sizeof__() / 1024)
        latencies.append(abs(timestamps[-1] - datetime.fromisoformat(send_timestamp)) / timedelta(milliseconds=1))

        total_size = sum(sizes[-100:])
        total_time = abs(timestamps[-100:][-1] - timestamps[-100:][0]).total_seconds()
        avg_latency = sum(latencies[-100:]) / len(latencies[-100:])
        avg_bandwidth = 0 if total_time == 0 else total_size / total_time

        print(f'## Received stats ## message size: {sizes[-1]} KB | average bandwidth: {avg_bandwidth} KB/s | average latency: {avg_latency} ms')


async def kafka_metrics(consumer):
    while True:
        await asyncio.sleep(1)
        metrics = consumer.metrics()
        print(f'## Kafka metrics: {metrics}')

async def kafka_metrics2():
    global sizes, latencies, timestamps

    while True:
        await asyncio.sleep(10)
        total_size = sum(sizes[-100:])
        total_time = abs(timestamps[-100:][-1] - timestamps[-100:][0]).total_seconds()
        avg_latency = sum(latencies[-100:]) / len(latencies[-100:])
        avg_bandwidth = 0 if total_time == 0 else total_size / total_time

        print(f'## Received stats ## message size: {sizes[-1]} KB | average bandwidth: {avg_bandwidth} KB/s | average latency: {avg_latency} ms')


async def kafka_consumer():
    consumer = KafkaConsumer(bootstrap_servers=['kafka-0:9092', 'kafka-1:9092', 'kafka-2:9092'], 
                                value_deserializer=msgpack.loads, 
                                # acks=1, # default 1
                                # compression_type='lz4', 
                                # retries=1,
                                # batch_size=16384 # default 16KB
                                )

    consumer.subscribe(['car_data'])

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(consume_data(consumer)), tg.create_task(kafka_metrics(consumer)), tg.create_task(kafka_metrics2())]

    metrics = consumer.metrics()
    pass

if __name__ == "__main__":
    logging.info('## Starting Kafka consumer...')

    asyncio.run(kafka_consumer())

    exit(0)
