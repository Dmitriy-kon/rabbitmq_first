import json
import aiormq


from color_formatter import color_f

async def send_message_to_external_main(message_dict: dict):
    print(f"{color_f.green}[ x ] Message: {message_dict} was sent to external main{color_f.default}")
    outcoming_message = json.dumps(message_dict).encode()
    
    connection = await aiormq.connect("amqp://rabbit")
    channel = await connection.channel()
    await channel.basic_publish(
        outcoming_message, routing_key="external_main:chat_message")
    await connection.close()