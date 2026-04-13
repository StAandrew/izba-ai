import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.joinpath("databases", "price_paid_data.db").resolve()
conn = sqlite3.connect(db_path)

# Step 2: Create a cursor object
cursor = conn.cursor()

# Step 3: Run a SELECT query to fetch data
# cursor.execute("SELECT AVG(price) FROM price_paid_data WHERE date_of_transfer LIKE '%/%/1995'")
cursor.execute("SELECT AVG(price) FROM price_paid_data WHERE date_of_transfer LIKE '2021-%-%'")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Step 4: Close the connection
conn.close()