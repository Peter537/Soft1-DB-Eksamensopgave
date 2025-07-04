# Database eksamensopgave - Online Marketplace

## GitHub Link

[https://github.com/Peter537/Soft1-DB-Eksamensopgave](https://github.com/Peter537/Soft1-DB-Eksamensopgave)

## Group

- Oskar (Ossi-1337, cph-oo221)
- Peter (Peter537, cph-pa153)
- Yusuf (StylizedAce, cph-ya56)

## Documentation

We have created:

- a Synopsis located in [synopsis.md](./synopsis.md)
- a Conceptual Database Design located in [conceptual diagram.md](./conceptual%20diagram.md)
- a Project Requirements document which includes a glossary, categories of users, functional and non-functional requirements, use-case diagram, and acceptance criterias in [project-requirements.md](./project-requirements.md)
- a description of the databases used in the project in [databases.md](./databases.md)
- a flow plan for the website of the project in [flowplan.md](./flowplan.md)

## Setup

1. Setup PostgreSQL, MongoDB, and Redis. See [docker-files/README.md](docker-files/README.md) for instructions if you don't have it set up already.
2. Install Python and the required packages. This project has been tested with Python 3.11.9 on a Python Virtual Environment (`python -m venv venv`). The required packages are listed in the [requirements.txt](./requirements.txt) file, and can be installed using pip (`pip install -r requirements.txt`).
3. Populate the databases with the provided script in [database-fill-scripts/script_runner.py](./database-fill-scripts/script_runner.py). This script will populate the PostgreSQL database with users and the MongoDB database with Products. You can run the script by executing `python script_runner.py` in the terminal from the [database-fill-scripts](./database-fill-scripts/) directory (Currently, this is the only way, since we use relative paths in the code).
4. Run the Streamlit application by executing `streamlit run src/app.py` in the terminal.
