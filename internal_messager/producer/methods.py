import json
import aiormq


from color_formatter import color_f

async def send_message_to_external_main(message_dict: dict):
    print(f"{color_f.green}[ x ] Message: {message_dict} was sent to external main from consumer{color_f.default}")
    
    message_dict |= {"source": "internal_messager"}
    outcoming_message = json.dumps(message_dict).encode()
    
    connection = await aiormq.connect("amqp://rabbit")
    channel = await connection.channel()
    
    await channel.basic_publish(
        outcoming_message, routing_key="external_main:chat_message")
    await connection.close()


async def send_pow_message_to_internal_worker(message_dict: dict):
    print(f"{color_f.green}[ x ] Message from consumer: {message_dict} was sent to internal worker from consumer{color_f.default}")
    
    message_dict |= {"source": "internal_messager"}
    
    out_message = json.dumps(message_dict).encode()
    
    connection = await aiormq.connect("amqp://rabbit")
    channel = await connection.channel()
    
    await channel.basic_publish(
        out_message, routing_key="internal_worker:pow_chat_massage")
    
    await connection.close()