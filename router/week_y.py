"""Example routes for learning general FastAPI inputs/outputs

CRUD Example

Note: this api will reset the dog_kennel when you restart the API
    the data in there is not persisted in a real database
"""
from fastapi import APIRouter, status, HTTPException, Body
from loguru import logger
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from uuid import uuid4, UUID
import datetime


router = APIRouter()

class DogBreedEnum(str, Enum):
    LABRADOR = 'Labrador Retriever'
    BEAGLE = 'Beagle'
    BULLDOG = 'Bulldog'
    POODLE = 'Poodle'
    GERMAN_SHEPARD = 'German Shepherd'

class MixinModelDefaults:
    """Entity Creation Bookeeping Mixin."""
    # default factory will create an id if one does not exist
    id: UUID = Field(default_factory=lambda: uuid4())
    created_at = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

default_config_dict = ConfigDict(
    extra='forbid',  # error if fields not defined below are provided
    str_strip_whitespace=True,  # trims extra whitespace to left/right of every input in model
    max_anystr_length = 255,  # longest any string can be
    use_enum_values=True
)

class DogSexEnum(str, Enum):
    """Sex of the dog using shorthand."""
    MALE="m"
    FEMALE="f"
    SPAYED="s"
    NEUTERED="n"
    UNKNOWN="u"


class Dog(BaseModel, MixinModelDefaults):
    model_config = default_config_dict # pydantic model settings
    # fields
    name: str
    breed: DogBreedEnum
    color: str = Field(min_length=1, max_length=20)
    age: int = Field(min=0, max=30)
    sex: DogSexEnum 
    description: str | None = None # using default max length from model_config

class DogCreateInput(BaseModel):
    model_config = default_config_dict # pydantic model settings
    # fields
    name: str
    breed: DogBreedEnum
    color: str = Field(min_length=1, max_length=20)
    age: int = Field(min=0, max=30)
    sex: DogSexEnum 
    description: str | None = None # using default max length from model_config

class DogUpdateInput(BaseModel):
    """Similar to the create model but all fields are optional."""
    model_config = default_config_dict # pydantic model settings
    # fields
    name: str | None = None
    breed: DogBreedEnum | None = None
    color: str | None = Field(default=None, min_length=1, max_length=20)
    age: int | None = Field(default=None,min=0, max=30)
    sex: DogSexEnum 
    description: str | None = None # using default max length from model_config


# this is our temporary storage
dog_kennel = dict[DogBreedEnum]()

# let's add 3 dogs so we have something when the API starts (for testing)
default_dogs = [
    Dog(
        name="Fido",
        breed=DogBreedEnum.GERMAN_SHEPARD,
        color="Black and Brown",
        age=3,
        sex=DogSexEnum.MALE,
    ),
    Dog(
        name="Spot",
        breed=DogBreedEnum.BULLDOG,
        color="Grey",
        age=7,
        description="Spot is an energetic dog for his age and loves long walks.",
        sex=DogSexEnum.NEUTERED
    ),
    Dog(
        name="Lana",
        breed=DogBreedEnum.POODLE,
        color="White",
        age=2,
        description="It is recommended that Lana does not live in a home with other dogs.",
        sex=DogSexEnum.SPAYED
    )
]

for dog in default_dogs:
    dog_kennel[dog.id] = dog

@router.post("/dogs")
async def crud_dog_create_example(
    new_dog: DogCreateInput = Body()
) -> Dog:
    """Create a dog!"""
    try:
        dog = Dog.model_validate(new_dog.model_dump())
        dog_kennel[dog.id] = dog
        return dog
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e

@router.get("/dogs")
async def crud_dog_list_example() -> list[Dog]:
    """Returns all dogs!"""
    try:
        return dog_kennel.values()
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e

@router.get("/dogs/{dog_id}")
async def crud_dog_get_example(dog_id: UUID) -> Dog:
    """Returns a single dog by ID!"""
    try:
        dog = dog_kennel.get(dog_id)
        logger.info(dog)
        if not dog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The dog you are looking for with id={dog_id} is not found!"
            )
        return dog
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e

@router.put("/dogs/{dog_id}")
async def crud_dog_edit_example(
    dog_id: UUID, 
    dog_update_values: DogUpdateInput = Body()
) -> Dog:
    """Update a dog by ID!"""
    try:
        dog: Dog | None = dog_kennel.get(dog_id)
        if not dog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The dog you are looking to update with id={dog_id} is not found!"
            )
        logger.info("Found dog to update %s", dog)
        update_json = dog_update_values.model_dump(exclude_none=True)
        logger.info("Fields to update on found dog %s", update_json)
        updated_dog = dog.model_copy(update=update_json)
        dog_kennel[dog.id] = updated_dog
        return updated_dog
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e
    
@router.delete("/dogs/{dog_id}")
async def crud_dog_delete_example(
    dog_id: UUID, 
) -> UUID:
    """Delete a dog by ID!"""
    try:
        # if you want to error that the dog exists you can
        #   but not erroring keeps this endpoint idempotent
        if dog_kennel.get(dog_id):
            del dog_kennel[dog_id]
        return dog_id
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e