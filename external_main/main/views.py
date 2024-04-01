from starlette.responses import JSONResponse
from color_formatter import color_f

async def main(request):
    print(request)
    print(dir(request))
    print(f"{color_f.red}Hello world{color_f.default}")
    return JSONResponse({"hello": "world"})