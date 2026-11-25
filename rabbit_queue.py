import json
import uuid
from datetime import datetime
from typing import Callable, Optional
import pika

RABBIT_HOST = "localhost"
QUEUE_NAME = "jobs_queue"


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def get_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials("guest", "guest")
    parameters = pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=8080,
        credentials=credentials,
    )
    return pika.BlockingConnection(parameters)


def setup_channel(connection: pika.BlockingConnection):
    channel = connection.channel()
    # durable=True chroni kolejkę przed utratą po restarcie kontenera RabbitMQ
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return channel


def add_job(description: str) -> dict:
    job = {
        "id": uuid.uuid4().hex[:8],
        "description": description,
        "status": "pending",
        "created_at": now(),
    }
    connection = get_connection()
    channel = setup_channel(connection)

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(job),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
        ),  # zapis wiadomości na dysku
    )
    connection.close()
    return job


def consume_jobs(
    consumer_name: str,
    work_callback: Callable[[dict], None],
    exit_when_empty: bool = False,
) -> None:
    connection = get_connection()
    channel = setup_channel(connection)
    # Konsument pobiera tylko 1 wiadomość naraz i czeka na kolejne dopiero po wysłaniu ACK
    channel.basic_qos(prefetch_count=1)

    if exit_when_empty:
        while True:
            method_frame, _, body = channel.basic_get(
                queue=QUEUE_NAME, auto_ack=False
            )
            if method_frame is None:
                break
            job = json.loads(body.decode("utf-8"))
            job["consumer"] = consumer_name
            work_callback(job)
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        return

    def on_message(ch, method, properties, body):
        job = json.loads(body.decode("utf-8"))
        job["consumer"] = consumer_name
        work_callback(job)
        # Potwierdzenie wykonania pracy dopiero teraz RabbitMQ usuwa ją z kolejki
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()
