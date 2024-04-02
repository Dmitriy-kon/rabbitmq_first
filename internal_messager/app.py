import asyncio

from starlette.applications import Starlette


from consumer.subscriptions import consumer_subs

class AmqpHttpServer(Starlette):
    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(consumer_subs())
        super().__init__(*args, **kwargs)
        
        
app = AmqpHttpServer(debug=True)