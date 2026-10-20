from pathlib import Path

import plotly
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

# plotly.js ships inside the python plotly package, so the browser and the
# server always use matching versions (and nothing is loaded from a CDN)
plotlyJsPath = Path(plotly.__file__).parent / "package_data" / "plotly.min.js"


@router.get("/vendor/plotly.min.js", include_in_schema=False)
def plotlyScript():
    return FileResponse(
        plotlyJsPath,
        media_type="application/javascript",
        headers={"Cache-Control": "public, max-age=86400"},
    )
