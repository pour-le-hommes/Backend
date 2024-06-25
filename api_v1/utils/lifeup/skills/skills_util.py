from api_v1.utils.database import init_db
import requests

class MyData(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
    
    def __init__(self):
        self._dbskills = None
        self._localskills = None
        self._tasks = None

    def dbskills(self):
        return self._dbskills
    
    def localskills(self):
        return self._localskills
    
    def input_dbskills(self,skills):
        self._dbskills = skills
        return "Skills have been stored"
    
    def input_localskills(self,skills):
        self._localskills = skills
        return "Skills have been stored"
    
def App_skills_retrieval():
    singletonInstance = MyData()

    skills = singletonInstance.localskills()
    try:
        query = requests.get("http://192.168.0.127:13276/skills")
        print(query)
        if query.status_code !=200:
            print(query.status_code)
            return None
        skills = eval(query.text.replace("id","liferpg_id"))["data"]
        singletonInstance.input_localskills(skills)
        return skills
    except Exception:
        return None


def Db_skills_retrieval():
    singletonInstance = MyData()

    db_skills = singletonInstance.dbskills()
    if db_skills == None:
        db = init_db()
        response = db.table('LifeRPG_Skills').execute()
        singletonInstance.input_dbskills(response.data)
        db_skills = response.data

    return db_skills

def Compare_DB_Local():
    db_skills = Db_skills_retrieval()
    app_skills = App_skills_retrieval()
    try:
        if len(db_skills)!=len(app_skills):
            db_skills = set([i["name"] for i in db_skills])
            app_skills = set([i["name"] for i in app_skills])

            if len(db_skills)>len(app_skills):
                return "Error, Local skills are missing",db_skills-app_skills
            else:
                return "Error, Database skills are missing",app_skills-db_skills
            
        else:
            return None
    except Exception as e:
        return e