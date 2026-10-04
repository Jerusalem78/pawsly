from src.repositories.pet import PetsRepository
from src.core.exceptions import NotFoundException, ForbiddenException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.pet import PetPostSchema, PetUpdateSchema
from uuid import UUID

class PetsService:

    def __init__(self, session : AsyncSession):
        self.session = session
        self.pet_repo = PetsRepository(session=session)

    def __check_pet(self, pet, user_id):

        if not pet:
            raise NotFoundException("Питомец не найден")

        if pet.owner_id != user_id:
            raise ForbiddenException("Это не ваш питомец")
    async def create_pet(self, user_id : UUID, data : PetPostSchema):

        pet = await self.pet_repo.create(
            name = data.name,
            spicies = data.spicies,
            breed = data.breed,
            age = data.age,
            special_notes = data.special_notes,
            owner_id = user_id
        )

        await self.session.commit()

        return pet

    async def get_my_pets(self, user_id : UUID, limit : int = 20, offset : int = 0):

        pets = await self.pet_repo.get_by_owner_id(
            owner_id = user_id,
            limit=20,
            offset=offset
        )

        return pets

    async def update_my_pet(self, user_id: UUID, pet_id: UUID, data: PetUpdateSchema):
        pet = await self.pet_repo.get_by_id(pet_id)

        self.__check_pet(pet=pet, user_id=user_id)

        payload = data.model_dump(exclude_none=True)
        if not payload:
            return pet

        pet = await self.pet_repo.update(pet_id, **payload)
        await self.session.commit()
        await self.session.refresh(pet)
        return pet

    async def delete_pet(self, pet_id: UUID, user_id: UUID):
        pet = await self.pet_repo.get_by_id(pet_id)
        self.__check_pet(pet=pet, user_id=user_id)
        pet = await self.pet_repo.delete(pet_id)
        await self.session.commit()
        return True if pet else False
    

        
