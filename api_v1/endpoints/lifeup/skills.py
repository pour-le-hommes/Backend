from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from api_v1.utils.database import init_db
from api_v1.utils.lifeup.skills.skills_functions import main_skill_retrieval, main_skill_update

skills_router = APIRouter()

@skills_router.get("/skills", description="Retrieve from the lifeup API or if not available then supabase")
def getSkills():
    try:
        response = main_skill_retrieval()
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse(e,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@skills_router.post("/update_skills", description="Updating the skills to Supabase, only available after /skills is used")
def updateSkills():
    try:
        response = main_skill_update()
        return response
    
    except Exception as e:
        return JSONResponse(e,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
