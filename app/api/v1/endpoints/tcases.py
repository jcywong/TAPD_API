from fastapi import APIRouter

router = APIRouter(prefix="/tcases", tags=["tcases"])

def get_tcases():
    return {"message": "Hello, World!"}