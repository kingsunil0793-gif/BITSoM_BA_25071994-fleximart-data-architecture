# FlexiMart Database Schema Documentation

## 1. Entity–Relationship Description

### ENTITY: customers
**Purpose:**  
Stores personal and contact information of customers registered on the FlexiMart platform.

**Attributes:**
- `customer_id` – Unique identifier for each customer (Primary Key)
- `first_name` – Customer’s first name
- `last_name` – Customer’s last name
- `email` – Unique email address of the customer
- `phone` – Standardized contact number
- `city` – City of residence
- `registration_date` – Date the customer registered

**Relationships:**
- One customer can place **many orders** (1:M relationship with orders table)

---

### ENTITY: products
**Purpose:**  
Stores product catalog information available for sale.

**Attributes:**
- `product_id` – Unique identifier for each product (Primary Key)
- `product_name` – Name of the product
- `category` – Product category (Electronics, Fashion, Groceries, etc.)
- `price` – Unit selling price
- `stock_quantity` – Available stock quantity

**Relationships:**
- One product can appear in **many order_items** (1:M relationship)

---

### ENTITY: orders
**Purpose:**  
Stores order-level transaction details.

**Attributes:**
- `order_id` – Unique order identifier (Primary Key)
- `customer_id` – Customer who placed the order (Foreign Key)
- `order_date` – Date when the order was placed
- `total_amount` – Total monetary value of the order
- `status` – Order status (Completed, Pending, Cancelled)

**Relationships:**
- One order belongs to **one customer**
- One order can contain **many order_items**

---

### ENTITY: order_items
**Purpose:**  
Stores item-level details for each order.

**Attributes:**
- `order_item_id` – Unique identifier (Primary Key)
- `order_id` – Related order (Foreign Key)
- `product_id` – Purchased product (Foreign Key)
- `quantity` – Number of units ordered
- `unit_price` – Price per unit at the time of purchase
- `subtotal` – Calculated as quantity × unit_price

**Relationships:**
- Many order_items belong to **one order**
- Many order_items reference **one product**

---

## 2. Normalization Explanation (Third Normal Form – 3NF)

The FlexiMart database schema is designed according to the principles of **Third Normal Form (3NF)** to ensure data consistency, eliminate redundancy, and improve data integrity.

### Functional Dependencies
- `customer_id → first_name, last_name, email, phone, city, registration_date`
- `product_id → product_name, category, price, stock_quantity`
- `order_id → customer_id, order_date, total_amount, status`
- `order_item_id → order_id, product_id, quantity, unit_price, subtotal`

Each non-key attribute depends solely on the primary key of its respective table.

### 3NF Justification
- **First Normal Form (1NF):** All attributes contain atomic values with no repeating groups.
- **Second Normal Form (2NF):** Each table has a single-column primary key, and all non-key attributes are fully dependent on that key.
- **Third Normal Form (3NF):** There are no transitive dependencies. Customer details are stored only in the `customers` table and not repeated in `orders`. Product information is stored separately in the `products` table and referenced through foreign keys.

### Anomaly Prevention
- **Update anomalies** are avoided because customer and product details are stored in only one place.
- **Insert anomalies** are prevented since customers and products can exist independently of orders.
- **Delete anomalies** are avoided because deleting an order does not remove customer or product records.

This normalized design ensures scalability, maintainability, and reliable analytics reporting.

---

## 3. Sample Data Representation

### customers

| customer_id | first_name | last_name | email                  | phone          | city      | registration_date |
|------------|------------|-----------|------------------------|----------------|-----------|-------------------|
| 1          | Rahul      | Sharma    | rahul.sharma@gmail.com | +91-9876543210 | Bangalore | 2023-01-15        |
| 2          | Priya      | Patel     | priya.patel@yahoo.com  | +91-9988776655 | Mumbai    | 2023-02-20        |

---

### products

| product_id | product_name       | category    | price   | stock_quantity |
|-----------|--------------------|-------------|---------|----------------|
| 1         | Samsung Galaxy S21 | Electronics | 45999.0 | 150            |
| 2         | Nike Running Shoes | Fashion     | 3499.0  | 80             |

---

### orders

| order_id | customer_id | order_date | total_amount | status    |
|---------|-------------|------------|--------------|-----------|
| 1       | 1           | 2024-01-15 | 45999.0      | Completed |
| 2       | 2           | 2024-01-16 | 5998.0       | Completed |

---

### order_items

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|--------------|----------|------------|----------|------------|----------|
| 1            | 1        | 1          | 1        | 45999.0    | 45999.0  |
| 2            | 2        | 2          | 2        | 2999.0     | 5998.0   |

