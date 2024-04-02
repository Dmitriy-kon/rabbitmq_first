import aiormq


from settings import AMQP_URI

from .methods import simple_message, simple_message_ack
from .color_formatter import color_f


async def consumer_subs():
    connection = await aiormq.connect(f"amqp://{AMQP_URI}")
    channel = await connection.channel()
    print(f"{color_f.red}Subscribing{color_f.default}")

    message_queue_declared = await channel.queue_declare(
        "internal_messager:test_message", durable=False
    )

    await channel.basic_consume(
        message_queue_declared.queue, simple_message, no_ack=True
    )

    message_queue_declared_ack = await channel.queue_declare(
        "internal_messager:test_message_ack", durable=False
    )

    await channel.basic_consume(
        message_queue_declared_ack.queue, simple_message_ack, no_ack=False
    )