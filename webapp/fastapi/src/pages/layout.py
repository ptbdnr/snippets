from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/layout")
templates = Jinja2Templates(directory="./src/templates")

@router.get("/", response_class=HTMLResponse)
async def get_handler(request: Request):
    return templates.TemplateResponse(request=request, name="layout.html")


if __name__ == "__main__":
    app = FastAPI()
    app.include_router(router)
