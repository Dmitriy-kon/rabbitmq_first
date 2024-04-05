import asyncio
import uuid
import json

import aiormq
import aiormq.types


class FibonacciRpcClient:
    def __init__(self) -> None:
        self.connection: aiormq.Connection = None
        self.channel: aiormq.Channel = None
        self.callback_queue = ""
        self.futures: dict[int, asyncio.Future] = {}
        self.loop = asyncio.get_event_loop()
    
    async def connect(self):
        self.connection = await aiormq.connect("amqp://rabbit")
        self.channel = await self.connection.channel()
        
        declare_ok = await self.channel.queue_declare(
            auto_delete=True,
            exclusive=True
        )
        
        await self.channel.basic_consume(
            declare_ok.queue,
            self.on_response,
        )
        
        self.callback_queue = declare_ok.queue
        
        return self
    
    async def on_response(self, message: aiormq.types.DeliveredMessage):
        future = self.futures.pop(message.header.properties.correlation_id)
        future.set_result(message.body)
        await self.channel.basic_ack(message.delivery.delivery_tag)
        await message.channel.queue_delete(message.routing_key)
    
    async def call(self, out_message_dict: dict, routing_key: str):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()
        
        self.futures[correlation_id] = future
        out_message_bytes = json.dumps(out_message_dict).encode()
        
        await self.channel.basic_publish(
            out_message_bytes,
            routing_key=routing_key,
            properties=aiormq.spec.Basic.Properties(
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue
            )
        )
        body = await future
        incoming_message_dict = json.loads(body)
        return incoming_message_dict
        