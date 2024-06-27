import ephem
import datetime
from api_v1.utils.database import init_db
from typing import List, Union
from api_v1.utils.lifeup.tasks.goals_n_tasks_singleton import TasksGoalsSingleton

SprintSingleton = TasksGoalsSingleton()
if SprintSingleton._goal_embeddings == []:
    SprintSingleton.goal_sync()


supadb = init_db()
sprint_goals_table = "Personal Sprint Goals"
sprint_goal_embedding_table = "Sprint Goals Embeddings"
sprint_tasks_table = "Tasks in Sprints"

def check_moon_requirement(date=None) -> List[Union[bool, float]]:
    if date is None:
        date = datetime.datetime.now()

    moon = ephem.Moon(date)
    phase = moon.moon_phase

    if phase>0.95 or phase<0.05:
        return [True, phase]
    else:
        return [False, phase]

# ? Sprint goals

def retrieve_goals(current_iteration:int) ->List[dict]:
    if SprintSingleton._goal!=[]:
        return SprintSingleton._goal

    result = supadb.table(sprint_goals_table).select("*").eq("iteration",current_iteration).execute()

    return result.data

def add_goals(current_iteration:int,name:str,desc:str | None):

    
    result = supadb.table(sprint_goals_table).insert(
        {
            "iteration": current_iteration,
            "sprint_goal": name,
            "description": desc,
        }
    ).execute()
    

    goal_embedding = SprintSingleton.add_goals(sprint_id=result.data[0]["id"], goal_name=name, goal_desc=desc)

    supadb.table(sprint_goal_embedding_table).insert(
        {
            "sprint_goal": result.data[0]["id"],
            "iteration": current_iteration,
            "embeddings": goal_embedding,
        }
    ).execute()

    SprintSingleton._goal.append(result.data)

    if result:
        return result.data
    

# ? Sprint tasks

def retrieve_tasks(current_iteration:int) ->List[dict]:
    result = supadb.table(sprint_tasks_table).select("*").eq("iteration",current_iteration).execute()

    return result.data

def add_tasks(current_iteration:int,name:str,desc:str | None,difficulty:int | None,importance:int | None):

    sprint_id = SprintSingleton.find_best_similar(name,desc)
    print("Sprint unique ID",sprint_id)
    result = supadb.table(sprint_tasks_table).insert(
        {
            "iteration": current_iteration,
            "sprint_goal":sprint_id,
            "name": name,
            "description": desc,
            "difficulty": difficulty,
            "importance": importance,
        }
    ).execute()

    if result:
        return result.data