from pymongo import MongoClient

def save_to_mongo(data, collection="scraped_data"):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["scraper_db"]

    db[collection].insert_many(data)
    print("Saved to MongoDB")