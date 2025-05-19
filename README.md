# Soft1-DB-Eksamen

## GitHub Link

[https://github.com/Peter537/Soft1-DB-Eksamensopgave](https://github.com/Peter537/Soft1-DB-Eksamensopgave)

## Group

- Oskar (Ossi-1337, cph-oo221)
- Peter (Peter537, cph-pa153)
- Yusuf (StylizedAce, cph-ya56)

## Description

Make a description of the project here?


## Setup

Before running any code, make sure that the following docker containers are running:

- MongoDB
- PostgreSQL
- Redis

To do this, go to the directory [docker-files](docker-files) and run the following command in the terminal:
```bash
docker-compose up -d
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