from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import config
from app.routers import assets, compare, pages, sector
from app.services.trust_score import getAllCompaniesWithTrust


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load the data, the model and every trust score once, so the first visitor isn't waiting
    getAllCompaniesWithTrust()
    yield


app = FastAPI(title="ESG Trust Score", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=config.staticDir), name="static")

app.include_router(pages.router)
app.include_router(compare.router)
app.include_router(sector.router)
app.include_router(assets.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
