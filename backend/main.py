from fastapi import FastAPI
from src.route import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.OM.bom import router as bom_router

app = FastAPI()
app.include_router(router)

app.mount("/webUI", StaticFiles(directory="../WebUI"), name="static")
app.include_router(bom_router, prefix="/api")

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
