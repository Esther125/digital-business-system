import uvicorn
from fastapi import FastAPI
from src.route import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

from src.customer import router as customer_router
from src.bom import router as bom_router
from src.componentInventory import router as component_inventory_router
from src.productinventory import router as product_inventory_router
from src.rfm import router as rfm_router
from src.order import router as order_router


logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


app = FastAPI(debug=True)
app.include_router(router)
app.mount("/webUI", StaticFiles(directory="../webUI"), name="static")

app.include_router(customer_router, prefix="/api", tags=["Customers"])
app.include_router(bom_router, prefix="/api", tags=["BOM"])
app.include_router(
    component_inventory_router,
    prefix="/api/component-inventory",
    tags=["Component Inventory"],
)
app.include_router(
    product_inventory_router,
    prefix="/api/product-inventory",
    tags=["Product Inventory"],
)
app.include_router(rfm_router, prefix="/api", tags=["RFM"])
app.include_router(order_router, prefix="/api", tags=["Orders"])


# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
