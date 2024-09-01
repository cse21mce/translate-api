import pymongo
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to connect to the MongoDB database
def connect_to_db():

    try:
        MONGO_URI = os.getenv("MONGO_URI")
        client = pymongo.MongoClient(MONGO_URI)
        db = client['pib']
        return db['press_releases']
    
    except Exception as e:
        # Handle any exceptions that occur during scraping
        raise str(e)



# Function to update translation status in the database
def update_translation_status(title, language, status):
    """
    Update the status of a specific translation for a press release in the database.
    
    :param title: The title of the press release (used to find the document).
    :param language: The language of the translation (e.g., 'hindi', 'urdu').
    :param status: The status of the translation (e.g., 'in-progress', 'completed', 'pending').
    """
    collection = connect_to_db()
    
    # Build the filter query to find the document by title
    filter_query = {"title": title}

    # Construct the update query to update the specific translation status
    update_query = {
        "$set": {
            f"translations.{language}.status": status
        }
    }

    # Update the document with the specific translation status
    result = collection.update_one(filter_query, update_query)
    
    if result.matched_count > 0:
        logger.info(f"Translation in '{language}' is '{status}'.")



# Function to store translation in the database
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
            f"translations.{language}": translation_data,
        }
    }

    # Update the document with the specific translation
    result = collection.update_one(filter_query, update_query, upsert=True)
    
    if result.matched_count > 0:
        logger.info(f"Translation in '{language}' is Completed.")
    


# Function to check if translation already exists in the database
def check_translation_in_db(title, lang):
    """
    Check if a specific translation for a press release already exists in the database.
    Raise an error if the title is not present in the database.

    :param title: The title of the press release (used to find the document).
    :param lang: The language of the translation (e.g., 'hindi', 'urdu').
    :return: The existing translation if found, None otherwise.
    """
    collection = connect_to_db()
        
    
    # Check if the specific translation exists
    translation_query = {"title": title, f"translations.{lang}": {"$exists": True}}
    result = collection.find_one(translation_query)
    
    if result:
        return result["translations"].get(lang)
    return None


def release_exist_with_title(title):
    """
    Check if a specific title for a press release already exists in the database.
    Raise an error if the title is not present in the database.

    :param title: The title of the press release (used to find the document).
    :return: The existing press release with title if found, None otherwise.
    """
    collection = connect_to_db()
    
    # First, check if the document with the title exists
    title_exists_query = {"title": title}
    document = collection.find_one(title_exists_query)
    
    if not document:
        return None
    else:
        return document