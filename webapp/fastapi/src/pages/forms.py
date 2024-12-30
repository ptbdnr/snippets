from typing import Annotated

from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter(prefix="/forms")
templates = Jinja2Templates(directory="./src/templates")

@router.get("/", response_class=HTMLResponse)
async def get_handler(request: Request):
    return templates.TemplateResponse(request=request, name="forms.html")

@router.post("/", response_class=HTMLResponse)
async def post_handler(
    request: Request,
    form_id: Annotated[str, Form()],
    letter: Annotated[str | None, Form()] = None,
    message: Annotated[str | None, Form()] = None,
):
    print(str(request), form_id, letter, message)
    match form_id:
        case "form_1":
            context={"result": {"label": "output", "content": f"{str(letter)} {str(message)}"}}
        case "form_4":
            context={"resultD": {"label": "D list", "content": "d list"}}

    return templates.TemplateResponse(
        request=request,
        name="forms.html",
        context=context
    )

class FormData(BaseModel):
    value: str

@router.post("/AB", response_class=JSONResponse)
async def post_ab_handler(
    request: Request,
    form_data: Annotated[FormData, Form()],
):
    match form_data.value:
        case "A":
            return {"resultAB": {"label": "A list", "content": "a list"}}
        case "B":
            return {"resultAB": {"label": "B list", "content": "b list"}}


if __name__ == "__main__":
    app = FastAPI()
    app.include_router(router)
