import asyncio
import json

from aiormq.abc import DeliveredMessage

from color_formatter import color_f
from producer.methods import send_message_to_external_main

async def simple_message(message: DeliveredMessage):
    print(f"{color_f.red}Message: {message.body}{color_f.default}")
    
async def simple_message_ack(message: DeliveredMessage):
    print(f"{color_f.red}Message with ack: {message.body}{color_f.default}")
    await message.channel.basic_ack(message.delivery.delivery_tag)


async def chat_massage(message: DeliveredMessage):
    await asyncio.sleep(0.5)
    
    message_data_dict = json.loads(message.body.decode())
    
    print(f"{color_f.red}[ x ] Message: {message_data_dict} and type {type(message_data_dict)} was received and been acked{color_f.default}")
    
    message_data_dict["message"] = message_data_dict["message"][::-1]
    
    await send_message_to_external_main(message_data_dict)
    await message.channel.basic_ack(message.delivery.delivery_tag)


async def json_message(message: DeliveredMessage):
    pass
    # json_message = json.loads(message.body.decode())
    # # json_message = message.body.decode
    # print(json_message.get("message"))
    # print(json_message.get("type"))
    
    # print(f"{color_f.red}Message: {json_message}{color_f.default}")
    # await message.channel.basic_ack(message.delivery.delivery_tag)