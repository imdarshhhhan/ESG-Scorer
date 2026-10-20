from pathlib import Path

import plotly
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


plotlyJsPath = Path(plotly.__file__).parent / "package_data" / "plotly.min.js"


@router.get("/vendor/plotly.min.js", include_in_schema=False)
def plotlyScript():
    return FileResponse(
        plotlyJsPath,
        media_type="application/javascript",
        headers={"Cache-Control": "public, max-age=86400"},
    )
