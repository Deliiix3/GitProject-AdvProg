import json

from app import broker, image_analysis, results


def handle_message(channel, method, properties, body) -> None:
    message = json.loads(body)
    job_id, url = message["job_id"], message["url"]
    print(f"Analizuję {job_id}: {url}")
    try:
        people = image_analysis.count_people(url)
        results.save_result(job_id, people)
        print(f"Gotowe {job_id}: osób = {people}")
    except Exception as error:
        results.save_result(job_id, None, str(error))
        print(f"Błąd {job_id}: {error}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    import pika

    connection = pika.BlockingConnection(broker.connection_parameters())
    channel = connection.channel()
    channel.queue_declare(queue=broker.QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=broker.QUEUE_NAME, on_message_callback=handle_message
    )
    print("Consumer czeka na prace (Ctrl+C kończy)")
    channel.start_consuming()


if __name__ == "__main__":
    main()
