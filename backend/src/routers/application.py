from fastapi import APIRouter, Depends
from src.services.application import ApplicationService
from src.services.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession 
from src.core.database import get_db
from src.schemas.application import ApplicationGetSchema, ApplicationPostSchema
from uuid import UUID
from typing import List

application_router = APIRouter(prefix="/application", tags=["application"])

def get_application_service(
        session : AsyncSession = Depends(get_db),
        ) -> ApplicationService:
    return ApplicationService(session)


@application_router.get("/my", response_model=List[ApplicationGetSchema])
async def get_my_application(
        offset : int = 0,
        limit : int = 20,
        service : ApplicationService = Depends(get_application_service),
        user = Depends(get_current_user),
) -> List[ApplicationGetSchema]:
    return await service.get_my_application(user_id=user.id, offset=offset, limit=limit)

@application_router.get('/get/{listing_id}', response_model=List[ApplicationGetSchema])
async def get_application_id(listing_id : UUID,
        user = Depends(get_current_user),
        service : ApplicationService = Depends(get_application_service)) -> List[ApplicationGetSchema]:
    return await service.get_listing_application(user_id=user.id, listing_id=listing_id)

@application_router.post("/create", response_model=ApplicationGetSchema)
async def create_application(
    data : ApplicationPostSchema,
    service : ApplicationService = Depends(get_application_service),
    user = Depends(get_current_user),
) -> ApplicationGetSchema:
    return await service.create_application(
        data=data
    )

@application_router.patch('/accept/{application_id}', response_model=ApplicationGetSchema)
async def accept_application(
    application_id : UUID,
    service : ApplicationService = Depends(get_application_service),
    user = Depends(get_current_user), 
    ) -> ApplicationGetSchema:
    return await service.accept_application(user_id=user.id, application_id=application_id)