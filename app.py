from fastapi import FastAPI
from translate import translate,translateIn
from pydantic import BaseModel

app = FastAPI()

languages = {
    # "assamese": "asm_Beng",
    # "kashmiri_arabic": "kas_Arab",
    # "kashmiri_devanagari": "kas_Deva",
    "punjabi": "pan_Guru",
    "bengali": "ben_Beng",
    # "sanskrit": "san_Deva",
    # "bodo": "brsx_Deva",
    # "maithili": "mai_Deva",
    # "santali": "sat_Olck",
    # "dogri": "doi_Deva",
    "malayalam": "mal_Mlym",
    # "sindhi_arabic": "snd_Arab",
    # "sindhi_devanagari": "snd_Deva",
    # "english": "eng_Latn",
    "marathi": "mar_Deva",
    # "konkani": "gom_Deva",
    # "manipuri_bengali": "mni_Beng",
    # "manipuri_meitei": "mni_Mtei",
    "tamil": "tam_Taml",
    "gujarati": "guj_Gujr",
    "telugu": "tel_Telu",
    "hindi": "hin_Deva",
    # "nepali": "npi_Deva",
    "urdu": "urd_Arab",
    "kannada": "kan_Knda",
    # "odia": "ory_Orya",
}


# Define translation endpoint
class Translation(BaseModel):
    text: str
@app.post("/translate")
async def translate_text(req: Translation):
    try:
        text = req.text.strip()

        if not text:
            return {"translation": text}

        translation_result = await translate(text)
        return translation_result

    except Exception as e:
        # If an exception occurs during translation, return an error response
        return {"error": str(e)}

    
@app.post("/translate/{lang}")
async def translate_text(lang:str,req:Translation):
    try:
        text = req.text.strip()

        if not text:
            return {"translation": text}
        
        if lang not in languages:
            return {"error": 'Language not found, unable to translate', "supported_languages":list(languages.keys())}

        translation_result = await translateIn(text,lang)
        return {"result":translation_result}

    except Exception as e:
        # If an exception occurs during translation, return an error response
        return {"error": str(e)}

    
