from fastapi import APIRouter

router = APIRouter()

@router.get("/sample")
async def sample_route():
    return {"message": "sample"}
