import logging
from typing import Union

import msgpack
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import random

from kafka3 import KafkaProducer
from kafka3.errors import KafkaError
from kafka import KafkaProducer

producer: Union[KafkaProducer, None] = None

FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

app = FastAPI(title="Kafka.Producer")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


def on_send_success(record_metadata):
    # Successful result returns assigned partition and offset
    logging.info(f"MESSAGE SENT: {record_metadata.topic} {record_metadata.partition} {record_metadata.offset}")

def on_send_error(excp):
    logging.error('MESSAGE ERROR: ', exc_info=excp)
    # handle exception

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.put("/kafka/{message_count}")
def update_item(message_count: int):

    # configure broker and serializer, msgpack provides better performance than json
    producer = KafkaProducer(bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'], value_serializer=msgpack.dumps, retries=1)

    # Asynchronous by default
    producer.send('msgpack-topic', {'key': 'value'}).add_callback(on_send_success).add_errback(on_send_error)

    random.seed(42)
    for _ in range(message_count):
        xyz = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        msg = {'some-key': b'some value', 'x': xyz[0], 'y': xyz[1], 'z': xyz[2]}
        producer.send('some-topic', msg).add_callback(on_send_success).add_errback(on_send_error)

    return {"message_count": message_count}

if __name__ == "__main__":
    logging.info("Kafka producer: app started")

    kwargs = {"host": "0.0.0.0", "port": 80}  # do not use Debug in production
    uvicorn.run(app, **kwargs)