"""Example routes for learning general FastAPI inputs/outputs

It is from Chapter 2 of Introducting Python 2nd Edition
https://learning.oreilly.com/library/view/introducing-python-2nd/9781492051374/ch02.html
"""
from fastapi import APIRouter, status, HTTPException, Depends, Body, Query
from loguru import logger
from typing import Any, Annotated
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from uuid import uuid4, UUID
import datetime

import time

router = APIRouter()

@router.post("/hello-world-example")
async def string_example(name: str) -> str:
    """Takes in a name and says hello!"""
    try:
        if name is not None:
            return f"Hello, {name}!"
        else:
            return f"Hello, World!"
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e

@router.post("/hello-world-example-2")
async def string_example(name: str | None = "World") -> str:
    """same as string_example() but uses World as a default input."""
    try:
        return f"Hello, {name}!"
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e

@router.post("/string-example")
async def string_example(first_name: str, last_name: str) -> str:
    """Take in two names and return them in title case as a full name."""
    try:
        return first_name.title() + " " + last_name.title()
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e

class StoogeEnum(str, Enum):
    MOE = 'Moe'
    LARRY = 'Larry'
    CURLY = 'Curly'

class FruitEnum(str, Enum):
    APPLE = '🍎'
    ORANGE = '🍊'
    BANANA = '🍌'
    WATERMELON = "🍉"

@router.post("/enum-example")
async def enum_example(stooge: StoogeEnum, fruit: FruitEnum) -> str:
    """
    As before, assign the value 7 to the name a. This creates an object box containing the integer value 7.

    Print the value of a.

    Assign a to b, making b also point to the object box containing 7.

    Print the value of b:
    """
    try:
        response = f"{stooge.value} ate the {fruit.value}"
        logger.info(response)
        return response
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e

@router.post("/tuple-example")
async def tuple_example(numbers_to_double: tuple[int | float]) -> str:
    """Take in tuple of ints or floats and doubles them."""
    try:
        return [n * 2 for n in numbers_to_double]
        # This is the same as the following code:

        # numbers_doubled = []
        # for n in numbers_to_double:
        #     numbers_doubled = n * 2
        # return numbers_doubled
    except Exception as e:
        logger.error("Error processing a: %s", str(e))
        raise e
