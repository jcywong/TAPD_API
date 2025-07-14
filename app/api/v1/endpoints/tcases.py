from fastapi import APIRouter

router = APIRouter(prefix="/tcases", tags=["tcases"])

@router.get("/")
def get_tcases():
    return {"message": "Hello, World!"}