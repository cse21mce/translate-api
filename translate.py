import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransTokenizer import IndicProcessor  # Assuming correct import path
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
"punjabi": "pan_Guru",
"bengali": "ben_Beng",
"malayalam": "mal_Mlym",
"marathi": "mar_Deva",
"tamil": "tam_Taml",
"gujarati": "guj_Gujr",
"telugu": "tel_Telu",
"hindi": "hin_Deva",
"urdu": "urd_Arab",
"kannada": "kan_Knda",
}

async def translate(text):

    input_sentences = text.split('.')[:-1] if '.' in text else [text]
    

    results = {}

    for tgt_lang in tgt_langs:

        batch = ip.preprocess_batch(input_sentences, src_lang=src_lang, tgt_lang=tgt_langs.get(tgt_lang))


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

        translations = ip.postprocess_batch(generated_tokens, lang=tgt_langs.get(tgt_lang))

        # Joining translations
        result = ""
        result = ''.join(translations)
        results[tgt_lang] = result.strip()

        print(tgt_lang,":",translations)

    return results

async def translateIn(text,tgt_lang):
    input_sentences = text.split('.')[:-1] if '.' in text else [text]

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
    result = ""
    result = ''.join(translations)
    print(tgt_lang,":",translations)
    return result.strip()

