import json


import aiocron


from chat.views import manager

# @aiocron.crontab("* * * * * */25", start=False)
@aiocron.crontab("*/2 * * * *", start=False)
async def one_minute_message():
    data = json.dumps({
        "group_id": "group_1",
        "username": "Admin",
        "message": "Hello from server!",
    })
    print("Data was sent")
    await manager.broadcast(data)