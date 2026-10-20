from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app import config
from app.services.company_service import getCompanyNames
from app.services.sector_service import buildSectorView, getSectorNames
from app.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def homePage(request: Request):
    companyNames = getCompanyNames()
    sectorNames = getSectorNames()
    defaultSector = config.defaultSector if config.defaultSector in sectorNames else sectorNames[0]

    context = {
        "companyNames": companyNames,
        "companyCount": len(companyNames),
        "sectorNames": sectorNames,
        "defaultSector": defaultSector,
        "sectorView": buildSectorView(defaultSector),
        "sectorCount": len(sectorNames),
        "dataPoints": config.heroDataPoints,
        "modelAccuracy": config.modelAccuracy,
    }
    return templates.TemplateResponse(request, "index.html", context)
