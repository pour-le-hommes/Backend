from api_v1.utils.database import init_db
import datetime as dt

db_todo = init_db()


def add_todos(task_name, task_desc):
    try:
        db_todo.table('website_todos').insert({"tasks":task_name,"complexity":task_desc}).execute()
    except ConnectionError as conn:
        raise conn
    
def update_todos(data_change):
    try:
        db_todo.table('website_todos').upsert(data_change).execute()
    except ConnectionError as conn:
        raise conn
    
def check_todos(force=False):
    todo_query = db_todo.table('website_todos').select("id","tasks","complexity","finished","finished_at").execute()
    return todo_query