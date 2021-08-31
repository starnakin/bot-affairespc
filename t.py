import json
from database import Database

config_file=json.load(open("./config.json"))
prefix = config_file["prefix"]
token = config_file["token"]

config_database=config_file["database"]
ip = config_database["ip"]
port = config_database["port"]
user = config_database["user"]
password = config_database["password"]
database = config_database["database"]

database = Database(ip, port, user, password, database)

for i in range (17):
    database.add_user_search(280098063643705345, f"https://affairespc.com/search?q=&cat={i}&price=0%2C10000")