import aiormq


from color_formatter import color_f
from .methods import rpc_pow_chat_massage



async def rpc_subscription():
    connection = await aiormq.connect("amqp://rabbit")
    channel = await connection.channel()
    print(f"{color_f.red} [*] Waiting for RPC requests.{color_f.default}")
    
    rpc_pow_queue_declared = await channel.queue_declare(
        "internal_worker:rpc_pow_chat_massage",
        durable=False
    )
    
    await channel.basic_consume(rpc_pow_queue_declared.queue, rpc_pow_chat_massage, no_ack=False)