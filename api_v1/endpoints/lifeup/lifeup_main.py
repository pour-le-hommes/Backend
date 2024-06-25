from fastapi import FastAPI, APIRouter
from api_v1.endpoints.lifeup.skills import skills_router
from api_v1.endpoints.lifeup.tasks import tasks_router

app = FastAPI()

lifeup_router = APIRouter(prefix="/lifeup", tags=["Life Up"])

# Include subdomain routers under the main router
lifeup_router.include_router(skills_router, prefix="/skills", tags=["Life Up","Skills"])
lifeup_router.include_router(tasks_router, prefix="/tasks", tags=["Life Up","Tasks"])