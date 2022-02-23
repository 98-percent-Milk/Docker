db.createUser(
    {
        user: "root",
        pwd: "MyNewPass1!",
        roles: [
            {
                role: "readWrite",
                db: "admin"
            }
        ]
    }
);



db = db.getSiblingDB('calulated_data');

db.createCollection('stats');

db.computed_stats.insertOne([
 {
    "Average Temp": "null",
    "Max Temp": "null",
    "Min Temp": "null"
  }]);