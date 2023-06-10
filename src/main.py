from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.generator import router as generator_router
from src.converter import router as converter_router

app = FastAPI(
    title="Graph generator",
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://gitlab.ost.ch/graph-analyzer/graphgenerator/-/blob/main/LICENSE",  # noqa
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}


app.include_router(generator_router.router)
app.include_router(converter_router.router)
