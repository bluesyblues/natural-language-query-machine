from query_machine import QueryMachine
import yaml

config_file_path = "./configs/dbconfigs.yaml"

with open(config_file_path) as f:
    config_list = yaml.load(f, Loader=yaml.FullLoader)


q = QueryMachine(
    config_list[0]
)
print(q.ask("Top 10 products in 2013"))
