from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from api_v1.api import init_db

health_router = APIRouter(tags=["Core"])

@health_router.get("/")
def main():
    return HTTPException(status_code=500)
    # return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)
    pass

@health_router.get("/health")
def health_check():
    supadb = init_db()
    print(supadb)
    return JSONResponse({"message":"Health check finished"})