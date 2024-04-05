import asyncio
import json

from aiormq.abc import DeliveredMessage

from color_formatter import color_f
from producer.methods import send_message_to_external_main, send_pow_message_to_internal_worker
from .helpers import FibonacciRpcClient

async def simple_message(message: DeliveredMessage):
    print(f"{color_f.red}Message: {message.body}{color_f.default}")
    
async def simple_message_ack(message: DeliveredMessage):
    print(f"{color_f.red}Message with ack: {message.body}{color_f.default}")
    await message.channel.basic_ack(message.delivery.delivery_tag)


async def chat_massage(message: DeliveredMessage):
    
    inc_message_data_dict = json.loads(message.body.decode())
    inc_message = inc_message_data_dict["message"]
    inc_user_name = inc_message_data_dict["username"]
    print(f"{color_f.red}RAD THIS IS Message: {inc_message_data_dict}{color_f.default}")
    
    if "!pow" in inc_message and inc_message_data_dict["source"] == "external_main":
        
        out_message_dict = {
            "message": inc_message,
            "username": inc_user_name
        }
        await send_pow_message_to_internal_worker(out_message_dict)
        await message.channel.basic_ack(message.delivery.delivery_tag)
    
    elif "!rpc" in inc_message:
        print(f"THIS IS MESSAGE from consumer {inc_message_data_dict} from rpc")
        out_message_dict = {
            "message": inc_message,
            "username": inc_user_name
        }
        fibbonaci_rpc = await FibonacciRpcClient().connect()
        message_dict = await fibbonaci_rpc.call(out_message_dict, "internal_worker:rpc_pow_chat_massage")
        
        await send_message_to_external_main(message_dict)
        await message.channel.basic_ack(message.delivery.delivery_tag)
        
        
    else:
        print(f"THIS IS MESSAGE from consumer {inc_message_data_dict}")
        
        if inc_message_data_dict["source"] == "external_main":
            out_message = inc_message[::-1]
        elif inc_message_data_dict["source"] == "internal_worker":
            out_message = inc_message
        
        out_message_dict = {
            "username": inc_user_name,
            "message": out_message,
        }
    
        print(f"{color_f.red}[ x ] Message: {out_message_dict} was received and sended to external main from consumer{color_f.default}")
    
    
        await send_message_to_external_main(out_message_dict)
        await message.channel.basic_ack(message.delivery.delivery_tag)

