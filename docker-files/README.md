# Docker Setup

- **PostgreSQL**

  1. Go to the directory [/postgres/](./postgres/) and run the following command in the terminal:
     ```bash
     docker-compose up -d
     ```

- **Redis**

  1. Go to the directory [/redis/](./redis/) and run the following command in the terminal:
     ```bash
     docker-compose up -d
     ```

- **MongoDB**

  1. Go to the directory [/mongo/](./mongo/) and run the following command in the terminal:
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
