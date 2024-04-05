import json

import aiormq

from color_formatter import color_f

async def send_message_to_queue(message_dict: dict):
    print(f"{color_f.green}[ x ] Message: {message_dict} was sent to interal messager from exernal main{color_f.default}")
    
    message_dict |= {"source": "external_main"}
    out_message_bytes = json.dumps(message_dict).encode()
    
    connection = await aiormq.connect("amqp://rabbit")
    channel = await connection.channel()
    
    
    # await channel.queue_declare(queue="external_messager:chat")
    await channel.basic_publish(
        out_message_bytes, routing_key="internal_messager:chat_message")
    
    
    await connection.close()