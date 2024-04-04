import json

import aiormq

from color_formatter import color_f
from settings import AMQP_URI

async def send_message_to_internal_messager(message_dict: dict):
    print(f"{color_f.green}[ x ] Message: {message_dict} was sent to internal_messager{color_f.default}")
    
    message_dict |= {"source": "internal_worker"}
    out_message_bytes = json.dumps(message_dict).encode()
    
    connection = await aiormq.connect(f"amqp://{AMQP_URI}")
    channel = await connection.channel()
    
    await channel.basic_publish(
        out_message_bytes, routing_key="internal_messager:chat_message"
    )
    
    await connection.close()