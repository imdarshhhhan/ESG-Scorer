from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.services.company_service import buildComparison
from app.templating import renderAlert, templates

router = APIRouter()


@router.get("/compare", response_class=HTMLResponse)
def compareCompanies(request: Request, company1: str = "", company2: str = ""):
    if not company1 or not company2:
        return renderAlert(request, "Please select both companies before comparing.", 400)

    if company1 == company2:
        return renderAlert(request, "Please select two different companies.", 400)

    comparison = buildComparison(company1, company2)
    if comparison is None:
        return renderAlert(request, "One of the selected companies was not found.", 404)

    return templates.TemplateResponse(
        request, "partials/compareResults.html", {"comparison": comparison}
    )
