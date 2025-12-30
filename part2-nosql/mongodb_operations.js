// mongodb_operations.js
// MongoDB Operations for Products Catalog

// Operation 1: Load Data
// mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray

// Operation 2: Basic Query
db.products.find(
  { category: "Electronics", price: { $lt: 50000 } },
  { _id: 0, name: 1, price: 1, stock: 1 }
);

// Operation 3: Review Analysis
db.products.aggregate([
  { $unwind: "$reviews" },
  {
    $group: {
      _id: "$name",
      avgRating: { $avg: "$reviews.rating" }
    }
  },
  { $match: { avgRating: { $gte: 4.0 } } }
]);

// Operation 4: Update Operation
db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user: "U999",
        rating: 4,
        comment: "Good value",
        date: new Date()
      }
    }
  }
);

// Operation 5: Complex Aggregation
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  { $sort: { avg_price: -1 } }
]);
