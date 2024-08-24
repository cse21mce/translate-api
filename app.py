from fastapi import FastAPI,BackgroundTasks
from translate import translate, translate_and_store  # Importing translation functions
from pydantic import BaseModel  # Importing BaseModel for request validation
from db import store_translation_in_db

app = FastAPI()  # Creating a FastAPI application instance

# Supported languages for translation
languages = {
    "hindi": "hin_Deva",
    "urdu": "urd_Arab",
    "punjabi": "pan_Guru",
    "gujarati": "guj_Gujr",
    "marathi": "mar_Deva",
    "telugu": "tel_Telu",
    "kannada": "kan_Knda",
    "malayalam": "mal_Mlym",
    "tamil": "tam_Taml",
    "odia": "ory_Orya",
    "bengali": "ben_Beng",
    "assamese": "asm_Beng",
    "manipuri_meitei": "mni_Mtei",
}

# Define translation endpoint for default translation service
class PressRelease(BaseModel):
    title: str 
    content: str 
    date_posted: str 
    ministry: str 



@app.post("/translate")
async def translate_text(req: PressRelease,background_tasks: BackgroundTasks):
    try:
        title = req.title.strip()
        content = req.content.strip()
        ministry = req.ministry.strip()

        if not title or not content or not ministry:
            return {"error": "Press Release is not complete. It must contain title, content and ministry"}  # If no text provided, return input text
        # Add the translate function to be run in the background
        
        
        background_tasks.add_task(translate, title, content, ministry)

        return {"message": "Translation process has started in the background."}


    except Exception as e:
        # If an exception occurs during translation, return an error response
        return {"error": str(e)}



# Define translation endpoint for specific language translation
@app.post("/translate/{lang}")
async def translate_text(lang: str, req: PressRelease, background_tasks: BackgroundTasks):
    try:
        if lang == 'english' or not lang:
            return req  # If the language is English or not provided, return the original request
        
        if lang not in languages:
            return {"error": 'Language not found, unable to translate', "supported_languages": list(languages.keys())}
        
        title = req.title.strip()
        content = req.content.strip()
        ministry = req.ministry.strip()

        background_tasks.add_task(translate_and_store, title, content, ministry, lang)

        return {"message": f"Translation to {lang} has started in the background."}


    except Exception as e:
        # If an exception occurs during translation, return an error response
        return {"error": str(e)}








# Start the FastAPI application using Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

