from fastapi import Request
from fastapi.templating import Jinja2Templates

from app import config

templates = Jinja2Templates(directory=str(config.templatesDir))


def renderAlert(request: Request, message: str, statusCode: int):
    #Small warning box that the browser drops into the results area
    return templates.TemplateResponse(
        request, "partials/alert.html", {"message": message}, status_code=statusCode
    )
