import asyncio

import aiormq


from aiormq.exceptions import AMQPConnectionError


from .methods import chat_massage_from_internal
from color_formatter import color_f



async def consumer_subs():
    print(f"{color_f.green}[ x ]Ready to consume messages{color_f.default}")
    
    
    while True:
        try:
            connection = await aiormq.connect("amqp://rabbit")
            break
        except AMQPConnectionError:
            await asyncio.sleep(5)
    channel = await connection.channel()
    
    chat_message_queue = await channel.queue_declare(
        "external_main:chat_message", durable=False
    )
    
    await channel.basic_consume(
        chat_message_queue.queue, chat_massage_from_internal, no_ack=False
    )
    