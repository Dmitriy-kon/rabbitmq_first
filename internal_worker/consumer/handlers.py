from consumer import methods
from consumer import schema


@schema.validate_req_schema(schema.Message)
async def pow_chat_message(validate_data, message):
    await methods.pow_chat_message(validate_data, message)