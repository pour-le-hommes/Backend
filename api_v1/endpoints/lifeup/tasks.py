import asyncio
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from core.schemas.lifeup.tasks_schemas import SuccessGetRequests, PostRequests, SuccessPostRequests, PostTasksRequests, SuccessTasksPostRequests
from api_v1.utils.lifeup.tasks.sprint_goals_functions import add_goals, check_moon_requirement, retrieve_goals, retrieve_tasks, add_tasks

tasks_router = APIRouter()


# ? Sprint tasks

@tasks_router.get("/{iteration}/sprint_goals", response_model=SuccessGetRequests, description="Retrieve sprint goals from the current iteration")
def get_sprint_goals(iteration: int):
    try:
        response = retrieve_goals(iteration)
        return SuccessGetRequests(data=response)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@tasks_router.post("/{iteration}/sprint_goals", description="Add sprint goals. Available only on full moons")
def update_sprint_goals(iteration:int,args:PostRequests):
    available, value = check_moon_requirement()
    if True:
        try:
            response = add_goals(iteration,args.sprint_name,args.sprint_desc)
            return SuccessPostRequests(data=response, response="A new goal has been set. New challenge awaits!") # type: ignore
        
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"You're entering a goal not in planning session. Right now it's {value}")


# ? Sprint tasks

@tasks_router.get("/{iteration}/tasks", response_model=SuccessGetRequests, description="Retrieve sprint task from the current iteration")
def get_sprint_tasks(iteration: int):
    try:
        response = retrieve_tasks(iteration)
        return SuccessGetRequests(data=response)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@tasks_router.post("/{iteration}/tasks", description="Add sprint goals. Available only on full moons")
def add_sprint_tasks(iteration:int,args:PostTasksRequests):
    try:
        response = add_tasks(current_iteration=iteration,name=args.sprint_name,desc=args.sprint_desc, importance=args.importance, difficulty=args.difficulty)
        return SuccessTasksPostRequests(data=response, response="A new tasks has been set. Ensure it's prepared!") # type: ignore
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))