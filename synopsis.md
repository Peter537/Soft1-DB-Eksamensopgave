# Synopsis: Online Marketplace with Polyglot Persistence

## Table of Contents

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

This project is about implementing a polyglot persistence system for an online marketplace, utilizing three different database technologies: PostgreSQL, MongoDB, and Redis.

The goal is to leverage the strengths of each database type to handle various data storage and retrieval needs effectively, ensuring a robust and scalable solution for managing user data, product listings, and session information.

As stated, the system idea is an online marketplace, similar to other online marketplaces, such as Amazon or eBay, where both users and companies have the ability to buy and sell products.

## 2. Project Domain & Requirements

**Domain:**
Online marketplace for buying and selling goods.

**Requirements:**
They can be found in the [project-requirements.md](./project-requirements.md) file, under the sections ["Functional Requirements"](./project-requirements.md#functional-requirements) and ["Non-Functional Requirements"](./project-requirements.md#non-functional-requirements).

## 3. Database Architecture & Technology Motivation

In this project, our system architecture is designed around three distinct database technologies, each chosen for their specific strengths in supporting different aspects of the marketplace platform. Before deciding on the database technologies, we created a [conceptual database diagram](./conceptual%20diagram.md) to visualize the relationships between the entities, and additionally, we created a [flow plan](./flowplan.md) to outline the user interactions with the different databases.

### 3.1 Relational Database (PostgreSQL)

We use PostgreSQL to store structured user data and product reviews. PostgreSQL's strong schema-guarantees ensure that critical information remains consistent and reliable.

In the context of the CAP theorem, PostgreSQL prioritizes consistency and availability, ensuring that all users see the same data and that the system remains accessible as long as there are no network partitions.

In our system, PostgreSQL manages user registration, authentication, and the storage of reviews linked to product postings from MongoDB.

By enforcing a clear relational model for users and reviews, we prevent inconsistencies in login logic and review submissions, and make it straightforward to aggregate and analyze user feedback.

This approach supports secure authentication, reliable user management, and accurate review data, forming a robust foundation for the marketplace's core user interactions.

### 3.2 NoSQL Document Database (MongoDB)

We use MongoDB to store product listings, taking advantage of its flexible, schema-less document model. This allows our marketplace to accommodate a wide variety of products, each with different attributes, without requiring rigid schema definitions or complex migrations.

In the context of the CAP theorem, MongoDB prioritizes consistency and partition tolerance, making it well-suited for distributed environments where data needs to remain correct and available across network partitions, though some operations may be temporarily unavailable during a partition.

By using MongoDB, we can easily add, modify, or remove product attributes as business-needs evolve, supporting rapid adaptation and efficient handling of unstructured or semi-structured data.

This flexibility enables our platform to scale and adapt quickly to changing requirements in the online marketplace.

### 3.3 In-Memory Database (Redis)

We use Redis to cache and store session-related and high-frequency data, such as shopping cart contents and product view counts. Redis' in-memory architecture allows us to access frequently used data with minimal latency, significantly improving performance for operations that require real-time responsiveness. We primarily chose Redis for its ability to efficiently handle short-lived data using built-in expiration (TTL), eliminating the need for manual cleanup of outdated records.

In the context of the CAP theorem, Redis in a single-node setup prioritizes consistency and partition tolerance, ensuring that data remains correct and accessible even in the presence of network partitions, though availability may be affected during such events. This makes Redis well-suited for scenarios where fast, consistent access to session and cache data is critical.

By leveraging Redis, we enhance the overall user experience with rapid access to shopping carts and real-time product view tracking, and we could further extend its use to cache frequent product searches for even greater responsiveness and scalability.

### 3.4 Integration

The 3 database types are integrated to provide seamless data flow across the platform. For example, when a user logs in, authentication is handled by PostgreSQL. During a purchase, product details are retrieved from MongoDB, the purchase is recorded in the user’s history, and the shopping cart stored in Redis is cleared. This integration enables us to utilize the unique strengths of each database while ensuring a consistent and unified user experience throughout the marketplace.

## 4. Data Population

To simulate a realistic online marketplace, we populated our databases using combination of 13 datasets, primarily sourced from Kaggle. These datasets included information relevant to users and products, but required some transformation to fit the specific data structures and requirements of our system.

To streamline deployment and ensure reproducibility, we developed a creation script that automatically sets up the database schemas and populates them with the prepared data. This approach enables anyone to quickly initialize the project environment and ensures that demonstrations and testing are consistent and reliable.

## 5. Demonstration & Deployment

All databases in this project were deployed using Docker containers in a local environment to ensure simplicity and reproducibility across different machines. This setup is ideal for development and demonstration purposes, but in a real-world scenario, the deployment architecture would need to be adapted for scalability, performance, and global reach.

For MongoDB, we chose a sharded cluster architecture to demonstrate how data can be distributed across multiple locations. In a production environment, this would allow us to place shards in different geographic regions (e.g., Denmark, New York, Shanghai), so users can access product data with lower latency from the nearest shard. This approach leverages MongoDB's strengths in partition tolerance and scalability (CP in CAP theorem), making it well-suited for handling large volumes of diverse product listings and supporting a global user base. However, our current setup uses single-node shards, which means we do not have full replica failover for each shard, which is something that would be necessary for high availability in a real deployment.

For Redis, we deployed a single instance, which is sufficient for local testing and demonstration. In a global system, however, it would be beneficial to use Redis Cluster or geo-distributed replicas to ensure that session data (such as shopping carts) is stored close to users in different regions. This would reduce latency and improve the user experience, especially for operations that require real-time responsiveness. Redis is typically configured for consistency and partition tolerance (CP in CAP theorem), but clustering would help address availability and scalability concerns as the system grows.

PostgreSQL was also deployed as a single instance, prioritizing consistency and availability (CA in CAP theorem). This is appropriate for user data and reviews, where it is critical to maintain a single source of truth and prevent inconsistencies. While sharding or replication could be considered for scaling reads or providing failover, it is generally preferable to keep user authentication and transactional data centralized to avoid conflicts and ensure data integrity.

The application itself is built using Streamlit, providing a simple and effective user interface that enables end-users to interact with all three databases. Key functionalities such as product search, and shopping cart operations can be demonstrated in a realistic scenario.

**Reflection:**  
Our deployment choices reflect a balance between simplicity for demonstration and the architectural considerations needed for a scalable, global online marketplace. In a real-world system, further steps would be needed to ensure high availability, low latency, and data consistency across regions, especially for MongoDB and Redis. PostgreSQL's role as the system's source of truth for user and review data makes its CA properties particularly valuable, while MongoDB and Redis would benefit from distributed setups to support a global user base.

## 6. Reflection: Pros & Cons

### 6.1 Business Perspective

#### 6.1.1 Pros

**Flexibility and Adaptability:**  
The use of MongoDB enables the business to quickly accommodate new product types and attributes without extensive database migrations or rigid schema changes. This agility is essential for responding to evolving market demands and maintaining a competitive advantage in a dynamic online marketplace.

**Enhanced User Experience:**  
Leveraging Redis for caching session data, such as shopping carts, ensures fast and efficient access, reducing latency and improving overall user satisfaction. Implementing caching for frequently accessed data (e.g., recently searched products) could further enhance responsiveness and performance.

#### 6.1.2 Cons

**Increased Operational Complexity:**  
Adopting a polyglot persistence strategy introduces additional complexity in system management. Maintaining multiple database technologies requires broader expertise, increased monitoring. This can be particularly challenging for smaller teams or organizations with limited resources.

**Integration and Maintenance Overhead:**  
Putting different databases together and keeping their data synchronized takes careful planning and constant work, which can raise costs and lead to mistakes.

### 6.2 Technical Perspective

#### 6.2.1 Pros

**Fault Isolation:**  
By distributing responsibilities across multiple databases, the system can achieve greater fault tolerance. If one database (e.g., PostgreSQL) experiences downtime or issues, other components (MongoDB and Redis) can continue functioning independently, improving overall system reliability.

**Scalability:**  
The architecture supports horizontal scaling for each database as needed (e.g., sharding MongoDB, clustering Redis). This modular approach allows for targeted scaling depending on which workload grows, leading to more efficient resource utilization.

**Optimized Performance:**
Each database is used according to its strengths, like relational integrity for users and reviews, document flexibility for products, and in-memory speed for session data, which results in improved performance for key operations.

#### 6.2.2 Cons

**Data Consistency Challenges:**  
It can be tricky to keep information consistent when you're using more than one database. When changes have to happen across different systems, you might need extra tools or custom code to make sure everything stays up-to-date.

**Complex Deployment and Debugging:**  
Running multiple databases makes deploying the system and finding bugs more difficult. If something breaks, it could be due to how the databases are talking to each other, not just a single system issue.

## 7. Conclusion

This project demonstrates the advantages of polyglot persistence in building a robust, scalable online marketplace. By leveraging PostgreSQL for consistent user and review data, MongoDB for flexible product listings, and Redis for fast session management, we utilize each database’s strengths to optimize performance and user experience.

The architecture enables seamless integration and adaptability to changing requirements. However, managing multiple databases introduces operational complexity and consistency challenges.

Overall, this approach provides agility and scalability, making it well-suited for modern, data-driven applications.
