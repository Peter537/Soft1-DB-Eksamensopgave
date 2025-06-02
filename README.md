# Soft1-DB-Eksamen

## GitHub Link

[https://github.com/Peter537/Soft1-DB-Eksamensopgave](https://github.com/Peter537/Soft1-DB-Eksamensopgave)

## Group

- Oskar (Ossi-1337, cph-oo221)
- Peter (Peter537, cph-pa153)
- Yusuf (StylizedAce, cph-ya56)

## Setup

Before running any code, make sure that the following containers for MongoDB, PostgreSQL, and Redis are running.

- **PostgreSQL**

  1. Go to the directory [docker-files/postgres/](docker-files/postgres/) and run the following command in the terminal:
     ```bash
     docker-compose up -d
     ```

- **Redis**

  1. Go to the directory [docker-files/redis/](docker-files/redis/) and run the following command in the terminal:
     ```bash
     docker-compose up -d
     ```

- **MongoDB**

  1. Go to the directory [docker-files/mongo/](docker-files/mongo/) and run the following command in the terminal:
     ```bash
     docker-compose up -d
     ```
  2. Run the following command in the terminal in the same directory, to initialize the config servers:

     ```bash
     Get-Content init-configsvr.js | docker exec -i mongo-sharded-cluster-configsvr1-1 mongosh
     ```

  3. Run the following command in the terminal in the same directory, to initialize the shards:
     ```bash
     Get-Content .\scripts\init-shards.js | docker exec -i mongo-sharded-cluster-mongos-1 mongosh
     ```

---

****Optional**:** It's recommended to use a virtual environment to avoid package conflicts. You can create a virtual environment using the following command:

```bash
python -m venv venv
```

To get the necessary packages, you need to run the following command in the terminal from the root directory of the project:

```bash
pip install -r requirements.txt
```

---

For reproducibility, we have a create script [script_runner.py](sql\scripts\script_runner.py), which populates the postgres database for users and mongodb for products.

To run the script, you need to do the following:

1. Go to the directory [sql\scripts](sql\scripts)
2. Open a terminal in the directory
3. Run the script with the command:

```bash
python script_runner.py
```

---

To run the streamlit app, you need to run the following command in the terminal:

1. Go to the directory [src](src)
2. Open a terminal in the directory
3. Run the command:

```bash
streamlit run app.py
```
