import json

from aiormq.abc import DeliveredMessage

from .prof_of_work import Pow
from producer.methods import send_message_to_internal_messager

async def pow_chat_message(message: DeliveredMessage):
    
    inc_message_dict = json.loads(message.body.decode())
    inc_message = inc_message_dict["message"]
    
    hash_res, calculate_elapsed_time = await Pow(inc_message).calculate()
    
    out_message_dict = {
        "username": "internal_messager",
        "message": f"POW {inc_message} hash: {hash_res} and elapsed time: {calculate_elapsed_time}",
    }
    
    await send_message_to_internal_messager(out_message_dict)
    await message.channel.basic_ack(message.delivery.delivery_tag)