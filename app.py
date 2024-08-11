from fastapi import FastAPI
from translate import translate, translateIn  # Importing translation functions
from pydantic import BaseModel  # Importing BaseModel for request validation

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
class Translation(BaseModel):
    text: str  # Request model to validate 'text' field

@app.post("/translate")
async def translate_text(req: Translation):
    try:
        text = req.text.strip()

        if not text:
            return {"translation": text}  # If no text provided, return input text

        translation_result = await translate(text)  # Call translate function
        return translation_result  # Return translation result

    except Exception as e:
        # If an exception occurs during translation, return an error response
        return {"error": str(e)}








# Define translation endpoint for specific language translation
@app.post("/translate/{lang}")
async def translate_text(lang:str, req: Translation):
    try:
        text = req.text.strip()

        if (not text or lang == 'english'):
            return {"result": text}  # If no text provided, return input text
        
        if lang not in languages:
            return {"error": 'Language not found, unable to translate', "supported_languages":list(languages.keys())}
        
        translation_result = await translateIn(text, lang)  # Call translateIn function for specified language
        return {"result": translation_result}  # Return translation result

    except Exception as e:
        # If an exception occurs during translation, return an error response
        return {"error": str(e)}







# Start the FastAPI application using Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

