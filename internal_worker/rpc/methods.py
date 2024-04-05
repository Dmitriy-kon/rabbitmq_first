import json

import aiormq
import aiormq.types

from color_formatter import color_f

async def rpc_pow_chat_massage(message: aiormq.types.DeliveredMessage):
    inc_message_dict = json.loads(message.body.decode())
    
    print(f"{color_f.red}[ x ]Message: {inc_message_dict} from worker rpc{color_f.default}")
    
    inc_message = inc_message_dict["message"]
    inc_username = inc_message_dict["username"]
    hash_res, calculate_elapsed_time = (1, 1)
    
    out_message_dict = {
        "username": inc_username,
        "message": f"POW {inc_message} hash: {hash_res} and elapsed time: {calculate_elapsed_time}",
        "source": "internal_worker",
    }
    
    out_message_bytes = json.dumps(out_message_dict).encode()
    
    await message.channel.basic_publish(
        out_message_bytes,
        routing_key=message.header.properties.reply_to,
        properties=aiormq.spec.Basic.Properties(
            correlation_id=message.header.properties.correlation_id,
        ),
    )
    await message.channel.basic_ack(message.delivery.delivery_tag)