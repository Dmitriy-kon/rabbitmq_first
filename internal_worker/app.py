import asyncio

from starlette.applications import Starlette


from consumer.subscription import consumer_subs


class AmpqHttpServer(Starlette):
    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(consumer_subs())
        super().__init__(*args, **kwargs)

app = AmpqHttpServer(debug=True)
    