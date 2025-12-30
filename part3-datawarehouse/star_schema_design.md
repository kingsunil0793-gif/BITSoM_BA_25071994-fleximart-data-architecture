# Star Schema Design for FlexiMart Data Warehouse

## Section 1: Schema Overview

**FACT TABLE: `fact_sales`**  
- **Grain:** One row per product per order line item  
- **Business Process:** Sales transactions  

**Measures (Numeric Facts):**  
- `quantity_sold`: Number of units sold  
- `unit_price`: Price per unit at the time of sale  
- `discount_amount`: Discount applied  
- `total_amount`: Final amount (quantity × unit_price − discount)  

**Foreign Keys:**  
- `date_key` → `dim_date`  
- `product_key` → `dim_product`  
- `customer_key` → `dim_customer`  

---

**DIMENSION TABLE: `dim_date`**  
- **Purpose:** Date dimension for time-based analysis  
- **Type:** Conformed dimension  
- **Attributes:**  
  - `date_key` (PK): Surrogate key (integer, format YYYYMMDD)  
  - `full_date`: Actual date  
  - `day_of_week`: Monday, Tuesday, etc.  
  - `month`: 1–12  
  - `month_name`: January, February, etc.  
  - `quarter`: Q1, Q2, Q3, Q4  
  - `year`: 2023, 2024, etc.  
  - `is_weekend`: Boolean  

---

**DIMENSION TABLE: `dim_product`**  
- **Purpose:** Product reference for sales analysis  
- **Type:** Conformed dimension  
- **Attributes:**  
  - `product_key` (PK): Surrogate key  
  - `product_id`: Original product ID from source  
  - `product_name`: Name of the product  
  - `category`: Product category (Electronics, Clothing, etc.)  
  - `brand`: Brand name  
  - `unit_price`: Standard selling price  

---

**DIMENSION TABLE: `dim_customer`**  
- **Purpose:** Customer reference for sales analysis  
- **Type:** Conformed dimension  
- **Attributes:**  
  - `customer_key` (PK): Surrogate key  
  - `customer_id`: Original customer ID from source  
  - `customer_name`: Full name  
  - `email`: Customer email  
  - `city`: City of residence  
  - `state`: State  
  - `country`: Country  
  - `customer_segment`: VIP, Regular, New  

---

## Section 2: Design Decisions

1. **Granularity:** The fact table is designed at the transaction line-item level, enabling detailed sales analysis for each product sold per order. This allows accurate aggregation by customer, product, or date and supports both high-level summaries and drill-down reports.  
2. **Surrogate Keys:** Surrogate keys are used instead of natural keys to ensure stable, unique identifiers independent of source system changes. They simplify joins and allow tracking slowly changing dimensions over time.  
3. **Analytical Support:** This star schema supports drill-down (e.g., year → quarter → month → day) and roll-up operations (e.g., sum sales by product category or region). Conformed dimensions enable consistent reporting across multiple fact tables in the future.  

---

## Section 3: Sample Data Flow

**Source Transaction:**  
- Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000  

**Transformed into Data Warehouse:**  

**fact_sales:**  
```json
{
  "date_key": 20240115,
  "product_key": 5,
  "customer_key": 12,
  "quantity_sold": 2,
  "unit_price": 50000,
  "discount_amount": 0,
  "total_amount": 100000
}
```

**dim_date:**  
```json
{
  "date_key": 20240115,
  "full_date": "2024-01-15",
  "day_of_week": "Monday",
  "month": 1,
  "month_name": "January",
  "quarter": "Q1",
  "year": 2024,
  "is_weekend": false
}
```

**dim_product:**  
```json
{
  "product_key": 5,
  "product_name": "Laptop",
  "category": "Electronics",
  "brand": "Generic",
  "unit_price": 50000
}
```

**dim_customer:**  
```json
{
  "customer_key": 12,
  "customer_name": "John Doe",
  "email": "johndoe@example.com",
  "city": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "customer_segment": "Regular"
}
```

