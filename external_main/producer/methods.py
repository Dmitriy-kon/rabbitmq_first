import aiormq

from color_formatter import color_f

async def send_message_to_queue(message: str):
    print(f"{color_f.green}[ x ] Message: {message} was sent to interal messager{color_f.default}")
    
    
    connection = await aiormq.connect("amqp://rabbit")
    channel = await connection.channel()
    message_bytes = message.encode()
    
    await channel.queue_declare(queue="test_queue")
    await channel.basic_publish(
        message_bytes, routing_key="internal_messager:test_chat",)
    await connection.close()