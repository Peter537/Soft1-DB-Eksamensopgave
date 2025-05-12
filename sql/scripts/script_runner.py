
from create_script_mongo import run_all_scripts as run_mongo_scripts
from create_script_postgress import run_all_scripts as run_postgres_scripts

if __name__ == "__main__":
    run_postgres_scripts()
    #run_mongo_scripts()

    print("-------------------------------------")
    print("All scripts executed successfully.")
