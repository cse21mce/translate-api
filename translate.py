
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransTokenizer import IndicProcessor 
import os


os.environ['CUDA_VISIBLE_DEVICES']='2, 3'


# Device selection
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
torch.cuda.empty_cache()

# Model and tokenizer initialization
model_name = "ai4bharat/indictrans2-en-indic-1B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True,force_download=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True,force_download=False).to(DEVICE)

# Preprocessing
ip = IndicProcessor(inference=True)

src_lang="eng_Latn"

tgt_langs = {
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

async def translateIn(text, tgt_lang):
    # Split text into sentences, ensuring the last part is included
    input_sentences = text.split('.')
    if input_sentences[-1] == '':
        input_sentences = input_sentences[:-1]  # Remove trailing empty string if present

    tgt_lang = tgt_langs.get(tgt_lang)

    batch = ip.preprocess_batch(input_sentences, src_lang=src_lang, tgt_lang=tgt_lang)

    # Tokenization and encoding
    inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        return_attention_mask=True,
    ).to(DEVICE)

    # Translation
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=5,
            num_return_sequences=1,
        )

    # Decoding and postprocessing
    with tokenizer.as_target_tokenizer():
        generated_tokens = tokenizer.batch_decode(
            generated_tokens.detach().cpu().tolist(),
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

    translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)

    # Joining translations
    result = ''.join(translations)
    return result.strip()

async def translate(text):
    # Split text into sentences, ensuring the last part is included
    input_sentences = text.split('.')
    if input_sentences[-1] == '':
        input_sentences = input_sentences[:-1]  # Remove trailing empty string if present
    
    results = {}

    for tgt_lang in tgt_langs:
        translation = await translateIn(text, tgt_lang)
        results[tgt_lang] = translation

    return results