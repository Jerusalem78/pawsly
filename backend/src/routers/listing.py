from fastapi import APIRouter, Depends
from src.services.listing import ListingService
from src.services.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession 
from src.core.database import get_db
from src.schemas.listing import ListingPostSchema, ListingGetSchema, ListingFilterSchema, ListingUpdateSchemas
from uuid import UUID
from typing import List

def get_listing_service(session : AsyncSession = Depends(get_db)) -> ListingService:
    return ListingService(session)

listing_router = APIRouter(prefix="/listing", tags=["listing"])

@listing_router.get("/", response_model=List[ListingGetSchema])
async def get_all_listing(
    offset : int = 0,
    limit : int = 20,
    filters: ListingFilterSchema = Depends(),
    service: ListingService = Depends(get_listing_service),
) -> list[ListingGetSchema]:
    return await service.get_listing(
        offset=offset,
        limit=limit,
        date_start=filters.date_start,
        date_end=filters.date_end,
        spicies=filters.spicies,
        min_price=filters.min_price,
        max_price=filters.max_price,
    )
    
@listing_router.post('/create', response_model=ListingGetSchema)
async def create_listing(data : ListingPostSchema,
        user = Depends(get_current_user),
        service : ListingService = Depends(get_listing_service)):
    return await service.create_listing(user_id=user.id, data=data)

@listing_router.get("/my", response_model=List[ListingGetSchema])
async def get_my_listing(limit : int =20,
        offset : int = 0 ,
        user= Depends(get_current_user),
        service : ListingService = Depends(get_listing_service)) -> List[ListingGetSchema]:
    return await service.get_my_listing(user_id=user.id, offset=offset, limit=limit)

@listing_router.patch("/edit/{listing_id}", response_model=ListingGetSchema)
async def change_listing(listing_id : UUID,
        data : ListingUpdateSchemas,
        user = Depends(get_current_user),
        service : ListingService = Depends(get_listing_service)) -> ListingGetSchema:
    return await service.update_my_listing(listing_id=listing_id, user_id=user.id, data=data)

@listing_router.patch("/close/{listing_id}", response_model=ListingGetSchema)
async def delete_listing(listing_id : UUID,
        user = Depends(get_current_user),
        service: ListingService = Depends(get_listing_service)) -> ListingGetSchema:
    return await service.close_listing(user_id=user.id, listing_id=listing_id)
