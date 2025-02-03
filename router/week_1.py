"""Routes for Week 1."""
from fastapi import APIRouter
from loguru import logger

router = APIRouter()

@router.get("/greet")
async def read_greeting():
    logger.info("Hello, Replit!")
    return {"message": f"Hello, Replit!"}

@router.get("/greet/{name}")
async def read_greeting_by_name(name: str):
    logger.info("Hello, Replit!")
    return {"message": f"Hello, {name}!"}