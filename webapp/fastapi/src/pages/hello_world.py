from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/hello_world")
templates = Jinja2Templates(directory="./src/templates")

@router.get("/", response_class=HTMLResponse)
async def get_handler(request: Request):
    return templates.TemplateResponse(request=request, name="hello_world.html")

@router.post("/", response_class=HTMLResponse)
async def post_handler(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="hello_world.html",
        context={"result": {"link": "https://www.wikipedia.org", "label": "wikipedia"}}
    )

if __name__ == "__main__":
    app = FastAPI()
    app.include_router(router)
