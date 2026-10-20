from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.services.sector_service import buildSectorView
from app.templating import renderAlert, templates

router = APIRouter()


@router.get("/sector", response_class=HTMLResponse)
def sectorResults(request: Request, name: str = ""):
    sectorView = buildSectorView(name)
    if sectorView is None:
        return renderAlert(request, "No companies found for this sector.", 404)

    return templates.TemplateResponse(
        request, "partials/sectorResults.html", {"sectorView": sectorView}
    )
