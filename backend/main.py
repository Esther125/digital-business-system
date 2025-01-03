import uvicorn
from fastapi import FastAPI
from src.route import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

from src.OM.bom import router as bom_router

app = FastAPI(debug=True)
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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
