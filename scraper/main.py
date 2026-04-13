import os
import sqlite3
import sys

from pydantic import BaseModel, Field
from typing import List
from firecrawl import FirecrawlApp
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

PAGES_TO_SCRAPE = 20
STOP_ON_ERROR = False


def add_listings_to_db(listings):
    db_file = 'scraped_listings.db'
    file_path = Path(__file__).resolve().parent.joinpath("backend", "databases", db_file).resolve()
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS listings (
           id TEXT PRIMARY KEY,
           url TEXT,
           number_of_bedrooms INTEGER,
           number_of_bathrooms INTEGER,
           title TEXT,
           description TEXT,
           property_type TEXT,
           address TEXT,
           postcode_short TEXT,
           postcode_long TEXT,
           price INTEGER,
           added_on TEXT,
           agent_name TEXT,
           agent_phone_number TEXT,
           image1_url TEXT,
           image2_url TEXT,
           image3_url TEXT,
           image4_url TEXT
       )
    ''')

    for listing in listings:
        cursor.execute('SELECT COUNT(1) FROM listings WHERE id = ?', (listing.id,))
        exists = cursor.fetchone()[0]

        if exists:
            print(f"Listing with id {listing.id} already exists. Skipping.")
        else:
            cursor.execute('''
                INSERT OR REPLACE INTO listings (
                    id, url, number_of_bedrooms, number_of_bathrooms, title, description, 
                    property_type, address, postcode_short, postcode_long, price, added_on, 
                    agent_name, agent_phone_number, image1_url, image2_url, image3_url, image4_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                listing.id,
                listing.url,
                listing.number_of_bedrooms,
                listing.number_of_bathrooms,
                listing.title,
                listing.description,
                listing.property_type,
                listing.address,
                listing.postcode_short,
                listing.postcode_long,
                listing.price,
                listing.added_on,
                listing.agent_name,
                listing.agent_phone_number,
                listing.image1_url,
                listing.image2_url,
                listing.image3_url,
                listing.image4_url
            ))

            conn.commit()
            print(f"Added {listing.id} to database.")
    conn.close()


def scrape_search_page(index=0):
    load_dotenv(find_dotenv())
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

    class PropertySchema(BaseModel):
        id: str = Field(..., alias="property_id")
        url: str = Field(..., alias="property_url_full")
        number_of_bedrooms: int = Field(..., alias="number_of_bedrooms")
        number_of_bathrooms: int = Field(..., alias="number_of_bathrooms")
        title: str = Field(..., alias="property_title")
        description: str = Field(..., alias="property_description", max_length=10000)
        property_type: str = Field(..., alias="property_type")
        address: str = Field(..., alias="property_address")
        postcode_short: str = Field(..., alias="property_postcode_short")
        postcode_long: str = Field(..., alias="property_postcode_full", min_length=6, max_length=8)
        price: int = Field(..., alias="property_price_per_month")
        added_on: str = Field(..., alias="added_on")
        agent_name: str = Field(..., alias="agent_name")
        agent_phone_number: str = Field(..., alias="agent_phone_number")
        image1_url: str = Field(..., alias="image1_url")
        image2_url: str = Field(..., alias="image2_url")
        image3_url: str = Field(..., alias="image3_url")
        image4_url: str = Field(..., alias="image4_url")

    class ListingsSchema(BaseModel):
        listings: List[PropertySchema]

    search_url = f"https://www.rightmove.co.uk/property-for-sale/find.html\
        ?searchLocation=Kensington+And+Chelsea+%28Royal+Borough%29&useLocationIdentifier=true\
        &locationIdentifier=REGION%5E61229&radius=0.0&_includeLetAgreed=on&includeLetAgreed=false&index={index}"

    print(f"Scraping...")
    data = app.scrape_url(search_url, {
        'formats': ['extract'],
        'timeout': 60 * 1000,  # milliseconds
        'actions': [
            {"type": "wait", "milliseconds": 5000},
        ],
        'extract': {
            'schema': ListingsSchema.model_json_schema(),
        }
    })

    listings = []
    for listing in data["extract"]["listings"]:
        listings.append(PropertySchema(**listing))
    add_listings_to_db(listings)


if __name__ == '__main__':
    for index in range(0, PAGES_TO_SCRAPE):
        try:
            scrape_search_page(index)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"Page {index} error:")
            print(e)
            if STOP_ON_ERROR:
                sys.exit(0)
