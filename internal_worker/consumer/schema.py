import json
import datetime


from pydantic import ValidationError, BaseModel, Field
from aiormq.abc import DeliveredMessage


from color_formatter import color_f


class Message(BaseModel):
    username: str = Field()
    message: str = Field()
    source: str = Field()


def validate_req_schema(request_schema):
    def wrap(func):
        async def wrapper(message: DeliveredMessage):
            start = datetime.datetime.now().time()
            
            json_data = None
            error = None
            
            try:
                json_data = json.loads(message.body.decode())
                print(f"{color_f.green}~ REQUEST: body={json_data}{color_f.default}")
                validate_data = request_schema.validate(json_data).dict()
            
            except ValidationError as er:
                error = f"~ ERROR REQUEST, VALIDATION ERROR: body={message.body} error={er}"
            except Exception as error_message:
                error = f"~ ERROR REQUEST: body={message.body} error={error_message}"

            if not error:
                try:
                    await func(validate_data, message)
                except Exception as error_message:
                    error = f"~ ERROR RESPONSE from not error: body={message.body} error={error_message}"

            if error:
                print(f"{color_f.red}{error}{color_f.default}")
            else:
                print(f"{color_f.green}~ SUCCESS RESPONSE: body={message.body}{color_f.default}")
        return wrapper
    return wrap