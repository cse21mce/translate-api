from fastapi import FastAPI,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from translate import translate, translate_and_store  # Importing translation functions
from pydantic import BaseModel  # Importing BaseModel for request validation
from db import release_exist_with_title


# Creating a FastAPI application instance
app = FastAPI(title="PIB Press Releases Translator", description="An API to translate PIB press releases.", version="1.0.0")  


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

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
        
        if(not release_exist_with_title(title)):
            raise Exception("Press Release with the title not exists in the database.")
        
        background_tasks.add_task(translate, title, content, ministry)

        return {"message": f"Translation has been started.","type":"info","success":True}


    except Exception as e:
        # If an exception occurs during translation, return an error response
        return {"message": str(e),"type":"error","success":False}



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


        if(not release_exist_with_title(title)):
            raise Exception("Press Release with the title not exists in the database.")

        background_tasks.add_task(translate_and_store, title, content, ministry, lang)
        # background_tasks.add_task(translate, title, content, ministry)


        return {"message": f"Translation to {lang} has been started.","type":"info","success":True}


    except Exception as e:
        # If an exception occurs during translation, return an error response
        return {"message": str(e),"type":"error","success":False}








# Start the FastAPI application using Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)

