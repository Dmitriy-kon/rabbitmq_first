import asyncio

import aiormq
from aiormq.exceptions import AMQPConnectionError

from color_formatter import color_f
from settings import AMQP_URI

from consumer.methods import pow_chat_message


async def consumer_subs():

    while True:
        try:
            connection = await aiormq.connect(f"amqp://{AMQP_URI}")
            break
        except AMQPConnectionError:
            await asyncio.sleep(5)
            
    channel = await connection.channel()
    print(f"{color_f.red}Connection was established from worker{color_f.default}")
    
    pow_chat_massage_queue_declared = await channel.queue_declare(
        "internal_worker:pow_chat_massage",
        durable=False
    )
    
    await channel.basic_consume(pow_chat_massage_queue_declared.queue, pow_chat_message, no_ack=False)
    
    