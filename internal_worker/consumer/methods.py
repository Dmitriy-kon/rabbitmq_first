import asyncio
import json


from concurrent.futures import ProcessPoolExecutor

from aiormq.abc import DeliveredMessage


from .prof_of_work import Pow
from producer.methods import send_message_to_internal_messager

executor = ProcessPoolExecutor(max_workers=4)


async def pow_chat_message(message_dict: dict, message: DeliveredMessage):
    inc_message_dict = message_dict
    inc_message = inc_message_dict["message"]

    loop = asyncio.get_event_loop()

    hash_res, calculate_elapsed_time = await loop.run_in_executor(
        executor, Pow(inc_message).calculate
    )

    # hash_res, calculate_elapsed_time = await Pow(inc_message).calculate()

    out_message_dict = {
        "source": "internal_worker",
        "username": inc_message_dict["username"],
        "message": f"POW {inc_message} hash: {hash_res} and elapsed time: {calculate_elapsed_time}",
    }

    await send_message_to_internal_messager(out_message_dict)
    await message.channel.basic_ack(message.delivery.delivery_tag)
