from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from api_v1.utils.database import init_db
from api_v1.utils.lifeup.skills.skills_util import MyData, App_skills_retrieval, Db_skills_retrieval

singletonInstance = MyData()
supadb = init_db()

potential_local_db = []

def main_skill_retrieval()->JSONResponse:
    try:
        myskills = App_skills_retrieval()
        if myskills !=None:
            return JSONResponse(myskills)
        response = Db_skills_retrieval()
        singletonInstance.input_localskills(response.data)
        return JSONResponse(response.data)
    except Exception as e:
        return JSONResponse(e,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def main_skill_update():
    try:
        # Query Local
        localquery = singletonInstance._localskills()
        if localquery is None:
            return JSONResponse("Query Failed. Link might not be found, ensure http://192.168.0.127:13276/skills is accessable",status_code=status.HTTP_404_NOT_FOUND)
        
        # Checking Singleton Function
        if singletonInstance._localskills == localquery:
            return JSONResponse("Data is already Updated",status_code=status.HTTP_404_NOT_FOUND)
        
        # Query DB
        response = supadb.table('LifeRPG_Skills').select("name","desc","level","exp","currentLevelExp","untilNextLevelExp","liferpg_id","icon","order","color","type").execute()

        # Updating Supabase main table
        total_data = []
        for each_skills in localquery:
            data, _ = supadb.table('LifeRPG_Skills_History').update(each_skills).eq("liferpg_id", each_skills["liferpg_id"]).execute()
            total_data.append(data)

        # Updating Supabase history table
        total_data = []
        for each_skills in localquery:
            data, _ = supadb.table('LifeRPG_Skills').update(each_skills).eq("liferpg_id", each_skills["liferpg_id"]).execute()
            total_data.append(data)

        # Updating Singleton Function
        singletonInstance.input_localskills(localquery)
        keys_to_extract = ["name","desc","level","exp","currentLevelExp","untilNextLevelExp"]
        filtered_local = [{key: eachskills[key] for key in keys_to_extract} for eachskills in localquery]
        singletonInstance.input_dbskills(filtered_local)

        return JSONResponse("Database Updated Successfully. Database, local singleton and db singleton is updated")
    except Exception as e:
        return JSONResponse(e,status_code=500)