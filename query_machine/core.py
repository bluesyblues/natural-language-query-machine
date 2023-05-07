
from query_machine.chatgpt import send_to_chatgpt
import query_machine.db as dbs
import json
import yaml
import openai


class QueryMachine:
    def __init__(self, config):
        self.name = config["name"]
        self.type = config["type"]
        self.connection = config["connection"]
        self.tables = config["tables"]
        # database
        db_class = getattr(dbs, self.type)
        self.db_instance = db_class(**self.connection)
        self.get_table_schema()

    def get_table_schema(self):
        if self.tables["table_schema_type"] == "yaml":
            with open(self.tables["table_schema_path"]) as f:
                self.table_schema = json.dumps(
                    yaml.load(f, Loader=yaml.FullLoader))
        elif self.tables["table_schema_type"] == "ddl":
            with open(self.tables["table_schema_path"]) as f:
                self.table_schema = f.read()
        else:
            raise Exception(
                f"no such schema type {self.tables['table_schema_type']}")

    def make_prompt(self, natural_language_query):
        return f"""We defined tables : {self.table_schema}, 
        make sql in {self.type} db language for next quote
        '{natural_language_query}'
        """

    # if you want to get sql only and no request to database required then use this
    def get_sql(self, natural_language_query):
        prompt = self.make_prompt(natural_language_query)
        try:
            response = send_to_chatgpt(prompt)
        except openai.error.APIConnectionError:
            response = send_to_chatgpt(prompt)

        try:
            ret = response.split("[")[1].split("]")[0]
        except:
            ret = response
        return ret

    def get_data(self, sql):
        return self.db_instance.send_query(sql)

    def ask(self, natural_language_query):
        sql_str = self.get_sql(natural_language_query)
        result = self.get_data(sql_str)
        return sql_str, result

    def info(self):
        return {
            "name": self.name,
            "type": self.type,
            "tables": self.table_schema,
        }
