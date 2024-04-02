
from aiormq.abc import DeliveredMessage

from .color_formatter import color_f

async def simple_message(message: DeliveredMessage):
    print(f"{color_f.red}Message: {message.body}{color_f.default}")
    
async def simple_message_ack(message: DeliveredMessage):
    print(f"{color_f.red}Message with ack: {message.body}{color_f.default}")
    # await message.channel.basic_ack(message.delivery.delivery_tag)