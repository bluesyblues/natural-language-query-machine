from query_machine import QueryMachine
import yaml
import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import csv
import os
from query_machine.db import SqliteDB
from datetime import datetime
from helper_methods import make_dirs

CONFIG_FILE_PATH = "./configs/dbconfigs.yaml"


history_db_path = "./history.db"
history_db = SqliteDB(history_db_path)
history_db.send_query("""
    CREATE TABLE IF NOT EXISTS history (
        request_id TEXT PRIMARY KEY,
        request_time TEXT,
        ip_address TEXT,
        request_query TEXT,
        sql TEXT,
        csv_path TEXT 
    );
""")


class QueryForm(BaseModel):
    db_id: str
    query: str


with open(CONFIG_FILE_PATH) as f:
    config_list = yaml.load(f, Loader=yaml.FullLoader)

db_dict = {str(uuid.uuid3(uuid.NAMESPACE_URL, conf["name"])): QueryMachine(
    conf) for conf in config_list}

templates = Jinja2Templates(directory="templates")
app = FastAPI()


async def log(request_id, ip_address, query, sql, csv_path):
    global history_db
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = sql.replace("'", "|")
    history_db.send_query(f"""
        INSERT INTO history (request_id, request_time, ip_address, request_query, sql, csv_path)
        VALUES ('{request_id}', '{current_time}', '{ip_address}', '{query}', '{sql}', '{csv_path}')
    """)


async def write_csv_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(data)


def updated_dict(original, to_updated):
    original.update(to_updated)
    return original


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    db_info = await get_db_info()
    db_info_list = [updated_dict(
        db_info[db_id], {"db_id": db_id}) for db_id in db_info]

    return templates.TemplateResponse("base.html", {"request": request, "db_info": db_info_list})


@app.get("/db")
async def get_db_info():
    return {db_id: db_dict[db_id].info() for db_id in db_dict}




@app.post("/query")
async def get_query_result(q: QueryForm, request: Request):
    result = db_dict[q.db_id].ask(q.query)
    request_id = str(uuid.uuid4())
    csv_path = f"./results/{request_id}.csv"
    make_dirs("./results/")
    await write_csv_file(csv_path, result[1])
    await log(request_id, request.client.host, q.query, result[0], csv_path)
    return {"sql": result[0], "request_id": request_id}


@app.get("/query/{request_id}")
async def download_result(request_id):
    file_path = f"./results/{request_id}.csv"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=400, detail="File not exists")
