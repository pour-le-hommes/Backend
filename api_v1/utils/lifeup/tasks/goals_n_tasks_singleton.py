from typing import List, Union
import numpy as np
from api_v1.utils.database import init_db
from api_v1.utils.cloudflare.main_function_cloudflare import text_embedding

def cosine_similarity(vecA, vecB):
    print("transform to np")
    vecA = np.array(eval(vecA))
    vecB = np.array(vecB)


    vecA = vecA.astype(float)
    vecB = vecB.astype(float)

    print("cal dot product")
    dot_product = np.dot(vecA, vecB)
    
    print("normalize value")

    normA = np.linalg.norm(vecA)
    normB = np.linalg.norm(vecB)
    
    print("calculating sim")
    similarity = dot_product / (normA * normB)
    
    return similarity


supadb = init_db()
sprint_goals_table = "Personal Sprint Goals"
sprint_goal_embedding_table = "Sprint Goals Embeddings"
sprint_tasks_table = "Tasks in Sprints"

class TasksGoalsSingleton():
    _instances = None
    _iteration : int
    _goal_embeddings : List
    _tasks : List

    def __new__(cls):
        if cls._instances is None:
            cls._instances = super(TasksGoalsSingleton, cls).__new__(cls)
            cls._instances._iteration = 0
            cls._instances._goal_embeddings = []
            cls._instances._tasks = []
            
        return cls._instances
    
    def goal_sync(self):
        if self._goal_embeddings == []:
            all_goals = supadb.table(sprint_goal_embedding_table).select("*").execute()
            sprint_vals = [i["iteration"] for i in all_goals.data] # type: ignore


            if sprint_vals!=[]:
                max_val = max(sprint_vals)
                self._iteration = max_val

                self._goal_embeddings = [[i["sprint_goal"],i["embeddings"]] for i in all_goals.data if i["iteration"]==max_val] # type: ignore
    
    def add_goals(self, sprint_id:int, goal_name:str, goal_desc:str | None):
        goal_added = "Goal Name: "+goal_name+" Goal Description: "
        if goal_desc:
            goal_added+=goal_desc

        goal_embed = text_embedding(text=goal_added)
        self._goal_embeddings.append([sprint_id, goal_embed])
        return goal_embed
    
    def find_best_similar(self,task_name:str, task_desc:str | None) ->int:
        if self._goal_embeddings != []:
            sprint_ids = [i[0] for i in self._goal_embeddings]
            goal_lists = [i[1] for i in self._goal_embeddings]

            task_full = "Goal Name: "+task_name+" Goal Description: "
            if task_desc:
                task_full+=task_desc

            task_embedding = text_embedding(text=task_full)

            cos_sim_list = [cosine_similarity(goal, task_embedding) for goal in goal_lists] # type: ignore

            print("finish cosine similarity", cos_sim_list)

            max_sim = max(cos_sim_list) # type: ignore

            print("max_sim",max_sim)

            return sprint_ids[cos_sim_list.index(max_sim)]


        else:
            raise IndexError