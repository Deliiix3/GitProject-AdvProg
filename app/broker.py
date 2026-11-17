import json
import os

QUEUE_NAME = "analyze_img"


def connection_parameters():
    import pika

    return pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        credentials=pika.PlainCredentials(
            os.getenv("RABBITMQ_USER", "guest"),
            os.getenv("RABBITMQ_PASSWORD", "guest"),
        ),
    )


def publish_job(job_id: str, url: str) -> None:
    """Producer - wrzuca pracę na kolejkę i od razu wraca."""
    import pika

    connection = pika.BlockingConnection(connection_parameters())
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps({"job_id": job_id, "url": url}),
            properties=pika.BasicProperties(delivery_mode=2),
        )
    finally:
        connection.close()
