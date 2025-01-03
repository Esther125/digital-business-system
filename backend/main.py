from fastapi import FastAPI
from src.route import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.OM.bom import app as bom_app

app = FastAPI()
app.include_router(router)

app.mount("/webUI", StaticFiles(directory="../WebUI"), name="static")
app.mount("/get-bom", bom_app)

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
