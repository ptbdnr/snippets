import time
from typing import Annotated

from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

_LOREM_IPSUM = """
This is formatted: **bold**, _italic_, and `code`. This is a [link](https://www.streamlit.io).

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu est quis turpis mattis aliquam a non justo. Sed libero nibh, lacinia dignissim tincidunt vel, congue vel erat. Pellentesque porta augue ac diam convallis, malesuada lacinia mi ultricies. Maecenas sodales odio vel lacinia pellentesque. Vivamus erat sapien, feugiat vitae orci euismod, accumsan imperdiet est. Nulla tempor erat mattis, mollis quam a, pellentesque magna. Cras lectus est, luctus non nisl nec, eleifend dictum risus. Aenean vestibulum posuere est, a ultricies ex consectetur nec. Nullam quis tempus diam. Quisque semper et sapien ac mollis. Nullam viverra risus a scelerisque imperdiet.

Vivamus eleifend scelerisque augue vitae egestas. Phasellus auctor nisi in lacus volutpat, id commodo leo auctor. Donec sit amet nisl nec leo pretium sollicitudin et sit amet risus. Sed in nisl eget nibh pretium vehicula in vel felis. Nunc ut scelerisque tortor, eu gravida diam. In hac habitasse platea dictumst. Nulla facilisi. Nam at augue nec velit laoreet rhoncus. Proin consectetur semper vulputate.
"""

router = APIRouter(prefix="/chat")
templates = Jinja2Templates(directory="./src/templates")

history = []

async def bot(history: list):
        bot_message = _LOREM_IPSUM
        # message
        history.append({"role": "assistant", "content": ""})
        for character in bot_message:
            history[-1]["content"] += character
            time.sleep(0.001)
            yield character

@router.get("/", response_class=HTMLResponse)
async def get_handler(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")

class FormData(BaseModel):
    value: str

@router.post("/stream", response_class=StreamingResponse)
async def post_ab_handler(
    form_data: Annotated[FormData, Form()],
):
    history.append({"role": "user", "content": form_data.value})
    return StreamingResponse(content=bot(history=history), media_type="text/event-stream")


if __name__ == "__main__":
    app = FastAPI()
    app.include_router(router)
