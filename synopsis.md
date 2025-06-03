### notes:
- Has to include CAP theorem
- The use of data diagrams before the database architecture
- Should we have a Table of Contents? (If so, fix it)


## Synopsis: Oline Marketplace with Polyglot Persistence

## Table of Contents:
1. [Introduction](#1-introduction)
2. [Project Domain & Requirements](#2-project-domain--requirements)
3. [Database Architecture & Technology Motivation](#3-database-architecture--technology-motivation)
   - [3.1 Relational Database (PostgreSQL)](#31-relational-database-postgresql)
   - [3.2 NoSQL Document Database (MongoDB)](#32-nosql-document-database-mongodb)
   - [3.3 In-Memory Database (Redis)](#33-in-memory-database-redis)
   - [3.4 Integration](#34-integration)
4. [Data Population](#4-data-population)
5. [Demonstration & Deployment](#5-demonstration--deployment)
6. [Reflection: Pros & Cons](#6-reflection-pros--cons)
   - [6.1 Business Perspective](#61-business-perspective)
   - [6.2 Technical Perspective](#62-technical-perspective)
7. [Conclusion](#7-conclusion)

## 1. Introduction
This project is about implementing a polyglot persistence system for an online marketplace, utilizing three different database technologies: PostgreSQL, MongoDB, and Redis. The goal is to leverage the strengths of each database type to handle various data storage and retrieval needs effectively, ensuring a robust and scalable solution for managing user data, product listings, and session information. As state the system idear is a online marketplace, similar to other online marketplaces, such as Amazon, eBay or DBA, where both users and companies can buy and sell products. 

## 2. Project Domain & Requirements

Idk skal dette afsnit bare være en sammenhængende text eller bare en liste over krav også lidt text like: "This is our requirements for the project.

Domain: <br>
Online marketplace for buying and selling goods.

Functional Requirements:

x

Non-Functional Requirements:

x


## 3. Database Architecture & Technology Motivation

In this project, our system architecture is designed around three distinct database technologies, each chosen for their specific strengths in supporting different aspects of the marketplace platform:


### 3.1 Relational Database (PostgreSQL)

We chose PostgreSQL to store structured user data and reviews because its ACID compliance and strong schema‐level guarantees ensure that critical information-such as user credentials, personal details, and aggregated ratings-remains correct and reliable. Without a single, well-defined relational model, it’s easy for authentication logic to fall into multiple, inconsistent login methods, and for review data to be submitted in varying formats that make it difficult to compute accurate averages or comparisons. By using PostgreSQL, we enforce one coherent data model, prevent drift in how users log in or submit feedback, and maintain a precise, dependable user experience.


### 3.2 NoSQL Document Database (MongoDB)

MongoDB is used for flexible storage of product listings. The marketplace must handle a wide variety of products, each with potentially different attributes. MongoDB’s schema less document model allows us to store products with diverse structures efficiently, enabling easy updates and the addition of new product types without the need for complex migrations, sush as if there is need for add, rename, or eliminate product attributes, there is no need to alter the entire database schema. This flexibility supports rapid business adaptation and a better fit for unstructured or semi-structured data.


### 3.3 In-Memory Database (Redis)

Redis is utilized for caching and storing session-related and high-frequency data, such as shopping cart content and product view count. We primary chose Redis for need to store data in short term, so we didn't have to use a database where we had to make sure that we removed it after a certain time, we could just have Redis remove it aftter a certain TTL. This allows us to quickly access frequently used data without the overhead of disk I/O, significantly improving performance for operations that require low latency, such as retrieving a user’s shopping cart or counting product views in real-time. Redis’s in-memory nature ensures that these operations are fast and efficient, enhancing the overall user experience. In addition, we could have used Redis for more frequent product searches, for reducing of retrieval times, which would have made the system more responsive and performant.

### 3.4 Integration

The 3 databases types are integrated to ensure seamless data flow. For example, on login a user is authenticated against PostgreSQL, and when a user completes a purchase, product details are fetched from MongoDB and save en its purchase history and the shopping car in redis is cleared. This integration allows us to leverage the strengths of each database while maintaining a coherent user experience across the platform.


## 4. Data Population

To simulate a realistic online marketplace, we populated our databases using combination of 13 datasets, primarily sourced from Kaggle. These datasets included information relevant to users and products, but required some transformation to fit the specific data structures and requirements of our system. 

To streamline deployment and ensure reproducibility, we developed a creation script that automatically sets up the database schemas and populates them with the prepared data. This approach enables anyone to quickly initialize the project environment and ensures that demonstrations and testing are consistent and reliable.


## 5. Demonstration & Deployment

All databases in this project were deployed using Docker containers in a local environment to ensure simplicity and reproducibility across different machines.

For MongoDB, we set up a sharded cluster architecture. This included three config servers configured as a replica set to provide failover for configuration data, and two shards, each running as a single-node replica set for horizontal data scaling. The mongos router was used to coordinate requests across the cluster, and Mongo Express was included for web-based database management. While this setup demonstrates MongoDB's sharding and configuration server failover, it does not implement full data replica failover on the shards themselves, as each shard only has a single member.

PostgreSQL and Redis were each deployed as single instances.

The application is built using Streamlit, providing a simple and effective user interface that enables both end-users and administrators to interact with all three databases. Key functionalities such as product search, user management, and shopping cart operations can be demonstrated in a realistic scenario.

## 6. Reflection: Pros & Cons

### 6.1 Business Perspective

#### 6.1.1 Pros:

__Flexibility and Adaptability:__  
    The use of MongoDB enables the business to quickly accommodate new product types and attributes without extensive database migrations or rigid schema changes. This agility is essential for responding to evolving market demands and maintaining a competitive advantage in a dynamic online marketplace.

__Enhanced User Experience:__  
    Leveraging Redis for caching session data, such as shopping carts, ensures fast and efficient access, reducing latency and improving overall user satisfaction. Implementing caching for frequently accessed data (e.g., recently searched products) could further enhance responsiveness and performance.

#### 6.1.2 Cons:

__Increased Operational Complexity:__  
    Adopting a polyglot persistence strategy introduces additional complexity in system management. Maintaining multiple database technologies requires broader expertise, increased monitoring. This can be particularly challenging for smaller teams or organizations with limited resources.

__Integration and Maintenance Overhead:__  
    Putting different databases together and keeping their data synced takes careful planning and constant work, which can raise costs and lead to mistakes.


### 6.2 Technical Perspective


#### 6.2.1 Pros:

__Fault Isolation:__  
    By distributing responsibilities across multiple databases, the system can achieve greater fault tolerance. If one database (e.g., PostgreSQL) experiences downtime or issues, other components (MongoDB and Redis) can continue functioning independently, improving overall system reliability.

__Scalability:__  
    The architecture supports horizontal scaling for each datastore as needed (e.g., sharding MongoDB, clustering Redis). This modular approach allows for targeted scaling depending on which workload grows, leading to more efficient resource utilization.


__Optimized Performance:__
    Each database is used according to its strengths-relational integrity for users and reviews, document flexibility for products, and in-memory speed for session data-resulting in improved performance for key operations.

#### 6.2.2 Cons:

__Data Consistency Challenges:__  
    It can be tricky to keep information consistent when you’re using more than one database. When changes have to happen across different systems, you might need extra tools or custom code to make sure everything stays up-to-date.

__Complex Deployment and Debugging:__  
    Running multiple databases makes deploying the system and finding bugs more difficult. If something breaks, it could be due to how the databases are talking to each other, not just a single system issue.

## 7. Conclusion

In conclusion, this project has demonstrated the benefits of adopting a polyglot persistence approach when designing a robust and scalable online marketplace. By utilizing PostgreSQL for secure handling of user data, MongoDB for flexible and adaptable product listings, and Redis for fast session management and caching, each database was able to play to its unique strengths and contribute to the overall effectiveness of the system.

The architecture supports seamless integration across these technologies, ensuring a unified and responsive user experience. This flexibility is especially valuable in a rapidly evolving marketplace environment, where requirements can change quickly. The system benefits from improved scalability, fault tolerance, and optimized performance.

However, the project also highlighted the inherent challenges of managing multiple databases, such as increased operational complexity, data consistency concerns, and more demanding deployment and debugging processes. These factors underscore the importance of thorough planning and a solid understanding of each technology involved.

Overall, while polyglot persistence introduces additional management requirements, its advantages in agility, scalability, and reliability make it a compelling choice for modern, data-driven applications such as online marketplaces.
