from src.routers.pets import pet_router
from src.routers.application import application_router
from src.routers.auth import auth_router
from src.routers.listing import listing_router
from src.routers.booking import booking_router
from src.routers.dispute import dispute_router
from src.routers.wallet import wallet_router
from src.routers.user import user_router
import uvicorn
from fastapi import FastAPI



app = FastAPI()
app.include_router(pet_router)
app.include_router(listing_router)
app.include_router(auth_router)
app.include_router(application_router)
app.include_router(booking_router)
app.include_router(dispute_router)
app.include_router(wallet_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)