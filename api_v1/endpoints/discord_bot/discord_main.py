from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse
from api_v1.utils.database import init_db
from api_v1.utils.discord_function.main_function import disc_main

discord_router = APIRouter(prefix="/discord",tags=["Discord Bot"])

@discord_router.get("/run_discord", description="Retrieve from the lifeup API or if not available then supabase")
def getSkills(backgroundtasks: BackgroundTasks):
    try:
        backgroundtasks.add_task(disc_main)
        return "Attempt to run discord"
    except Exception as e:
        return JSONResponse(e,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)