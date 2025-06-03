# Database eksamensopgave -

## GitHub Link

[https://github.com/Peter537/Soft1-DB-Eksamensopgave](https://github.com/Peter537/Soft1-DB-Eksamensopgave)

## Group

- Oskar (Ossi-1337, cph-oo221)
- Peter (Peter537, cph-pa153)
- Yusuf (StylizedAce, cph-ya56)

## Setup

1. Setup PostgreSQL, MongoDB, and Redis. See [docker-files/README.md](docker-files/README.md) for instructions if you don't have it set up already.
2. Install Python and the required packages. This project has been tested with Python 3.11.9 on a Python Virtual Environment (`python -m venv venv`). The required packages are listed in the [requirements.txt](./requirements.txt) file, and can be installed using pip (`pip install -r requirements.txt`).
3. Populate the databases with the provided script in [database-fill-scripts/script-runner.py](./database-fill-scripts/script_runner.py). This script will populate the PostgreSQL database with users and the MongoDB database with Products. You can run the script by executing `python database-fill-scripts/script_runner.py` in the terminal.
4. Run the Streamlit application by executing `streamlit run src/app.py` in the terminal.
