import sqlite3
import pandas as pd
from pathlib import Path

columns = [
    "transaction_unique_id",
    "price",
    "date_of_transfer",
    "postcode",
    "property_type",
    "old_new",
    "duration",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category_type",
    "record_status"
]

# Step 1: Load the CSV file into a pandas DataFrame
csv_file = Path(__file__).resolve().parent.joinpath("data", "kensington_chelsea_price_paid_data.csv").resolve()
df = pd.read_csv(csv_file)

df["date_of_transfer"] = df["date_of_transfer"].apply(lambda x: x.split(" ")[0])

# Step 2: Connect to SQLite database (or create it if it doesn't exist)
db_path = Path(__file__).resolve().parent.joinpath("databases", "price_paid_data.db").resolve()
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 3: Convert the DataFrame into a SQL table
df.to_sql('price_paid_data', conn, if_exists='append', index=False)

# Step 4: Commit changes and close the connection
conn.commit()
conn.close()

print("CSV file successfully loaded into SQLite database!")