import pymongo
import os

def connect_to_db():

    try:
        MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        client = pymongo.MongoClient(MONGO_URI)
        # print("MongoDB Client:", client)
        db = client['pib']
        return db['press_releases']
    
    except Exception as e:
        # Handle any exceptions that occur during scraping
        raise str(e)


def store_translation_in_db(title, language, translation_data):
    """
    Store a specific translation for a press release in the database.
    
    :param title: The title of the press release (used to find the document).
    :param language: The language of the translation (e.g., 'hindi', 'urdu').
    :param translation_data: A dictionary containing the translated fields (e.g., title, content, ministry).
    """
    collection = connect_to_db()
    
    # Build the filter query to find the document by title
    filter_query = {"title": title}

    # Construct the update query to update the specific translation
    update_query = {
        "$set": {
            f"translations.{language}": translation_data
        }
    }

    # Update the document with the specific translation
    result = collection.update_one(filter_query, update_query, upsert=True)
    
    if result.matched_count > 0:
        print(f"Translation in '{language}' for title '{title}' updated successfully.")
    else:
        print(f"Document with title '{title}' inserted with a new translation in '{language}'.")
    


# Function to check if translation already exists in the database
def check_translation_in_db(title, lang):
    collection = connect_to_db()
    query = {"title": title, f"translations.{lang}": {"$exists": True}}
    result = collection.find_one(query)
    
    if result:
        return result["translations"].get(lang)
    return None