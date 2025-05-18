import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)
sys.path.append("./mongo")
sys.path.append(os.path.join(project_root, "src"))

from mongo.create_script_mongo import run_all_scripts as run_mongo_scripts
from postgres.create_script_postgres import run_all_scripts as run_postgres_scripts
from src.db.redis.zincrby import delete_all_views

if __name__ == "__main__":
    delete_all_views()
    run_postgres_scripts()
    run_mongo_scripts()

    print()
    print("-------------------------------------")
    print("All scripts executed successfully.")
