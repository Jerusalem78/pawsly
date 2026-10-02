from fastapi import APIRouter, Depends
from src.services.pet import PetsService
from src.services.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession 
from src.core.database import get_db
from src.schemas.pet import PetPostSchema, PetGetSchema, PetUpdateSchema
from uuid import UUID
from typing import List

def get_pets_service(session : AsyncSession = Depends(get_db)) -> PetsService:
    return PetsService(session)

pet_router = APIRouter(prefix="/pets", tags=["pets"])

@pet_router.post("/create", response_model=PetGetSchema)
async def create_pet(data : PetPostSchema,
        service : PetsService = Depends(get_pets_service),
        user = Depends(get_current_user)) -> PetGetSchema:
    return await service.create_pet(user_id=user.id, data=data)

@pet_router.get("/mypets", response_model=List[PetGetSchema])
async def get_my_pets(limit : int = 20,
        offset : int = 0,
        service : PetsService = Depends(get_pets_service),
        user = Depends(get_current_user)) -> List[PetGetSchema]:

    return await service.get_my_pets(user_id=user.id, offset=offset, limit=limit)

@pet_router.patch("/edit/{pet_id}", response_model=PetGetSchema)
async def change_pet(
    pet_id: UUID,
    data: PetUpdateSchema,
    service: PetsService = Depends(get_pets_service),
    user=Depends(get_current_user),
) -> PetGetSchema:
    return await service.update_my_pet(user_id=user.id, pet_id=pet_id, data=data)

@pet_router.delete("/delete/{pet_id}")
async def delete_pet(
    pet_id : UUID,
    service : PetsService = Depends(get_pets_service),
    user=Depends(get_current_user)
) -> bool:
    return await service.delete_pet(pet_id, user_id=user.id)