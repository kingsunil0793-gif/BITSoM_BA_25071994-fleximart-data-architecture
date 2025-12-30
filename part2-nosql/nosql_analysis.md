# NoSQL Analysis for FlexiMart

## Section A: Limitations of RDBMS (≈150 words)

Relational databases such as MySQL rely on a fixed and predefined schema, which makes them less suitable for highly diverse product catalogs. In FlexiMart’s case, different products require different attributes—laptops need specifications like RAM, processor, and storage, while shoes require size, color, and material. Representing this diversity in an RDBMS often leads to wide tables with many NULL values or the creation of multiple related tables, increasing complexity and reducing performance.

Frequent schema changes are another challenge. Adding new product types or attributes requires ALTER operations, which can be time-consuming, may lock tables, and often require downtime. Additionally, storing customer reviews as nested or hierarchical data is inefficient in RDBMS because relational systems are optimized for flat, normalized data. Reviews typically need separate tables and multiple joins, which negatively impacts read performance and complicates queries. These constraints make traditional relational databases less flexible for rapidly evolving, heterogeneous product data.

Sources:
https://severalnines.com/blog/mysql-vs-mongodb-when-use-nosql
https://www.mongodb.com/resources/compare/relational-vs-nosql


## Section B: NoSQL Benefits (≈150 words)

MongoDB addresses these limitations through its document-oriented NoSQL architecture. Its flexible schema allows each product to be stored as a document with its own structure, enabling laptops, shoes, and other products to coexist in the same collection without enforcing uniform attributes. New fields can be added at any time without schema migrations, making MongoDB ideal for frequently changing product catalogs.

MongoDB also supports embedded documents, allowing customer reviews to be stored directly within product documents as nested objects or arrays. This design eliminates complex joins and enables faster read operations by retrieving all relevant product and review data in a single query. Furthermore, MongoDB is designed for horizontal scalability using sharding, which distributes data across multiple servers. This ensures high availability and performance as FlexiMart’s catalog and user base grow. Together, these features make MongoDB well suited for managing diverse, dynamic, and nested data structures.

Sources:
https://www.mongodb.com/docs/manual/core/data-modeling-introduction/
https://www.mongodb.com/why-use-mongodb


## Section C: Trade-offs (≈100 words)

Despite its advantages, MongoDB has notable disadvantages compared to MySQL. First, while MongoDB supports transactions, traditional relational databases provide stronger and more mature ACID guarantees, especially for complex multi-table operations. This can be a limitation when strict consistency is critical.

Second, MongoDB does not support complex SQL-style joins, which can make handling highly relational data more difficult and may require data duplication through denormalization. This can increase storage usage and make data maintenance more challenging. Therefore, MongoDB may not be ideal for applications that heavily rely on complex relational queries and strict transactional consistency.

Sources:
https://www.geeksforgeeks.org/difference-between-mysql-and-mongodb/
https://www.pvpsiddhartha.ac.in/dep_it/lecture%20notes/3-2-23/MWA/UNIT-5.pdf
