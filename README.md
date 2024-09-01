# Translate-API

## Setup Locally

```bash
git clone https://github.com/cse21mce/translate-api.git
```

## Package Installatoin

```bash
pip install fastapi
pip install pydantic
pip install torch
pip install transformers
git clone https://github.com/VarunGumma/IndicTransToolkit
cd IndicTransToolkit

pip install --editable ./
```

## Usage

1. Endpoint (/translate) -> http://127.0.0.1:8000/translate

---

---

```json
body : {
    "text": "The quick brown fox jumps over the lazy dog."
}

response: {
  "hindi": "तेज़ भूरा लोमड़ी आलसी कुत्ते के ऊपर से कूदती है",
  "urdu": "تیز بھوری لومڑی سست کتے پر چھلانگ لگا دیتی ہے",
  "punjabi": "ਤੇਜ਼ ਭੂਰੇ ਲੂੰਬਡ਼ੀ ਆਲਸੀ ਕੁੱਤੇ ਉੱਤੇ ਛਾਲ ਮਾਰਦੀ ਹੈ",
  "gujarati": "ઝડપી ભુરો શિયાળ આળસુ કૂતરા પર કૂદી પડે છે",
  "marathi": "वेगवान तपकिरी कोल्हा आळशी कुत्र्यावर उडी मारतो",
  "telugu": "వేగవంతమైన గోధుమ రంగు నక్క సోమరితనం కుక్కపైకి దూకుతుంది",
  "kannada": "ತ್ವರಿತ ಕಂದು ಬಣ್ಣದ ನರಿ ಸೋಮಾರಿಯಾದ ನಾಯಿಯ ಮೇಲೆ ಜಿಗಿಯುತ್ತದೆ",
  "malayalam": "തിടുക്കത്തിലുള്ള തവിട്ടുനിറമുള്ള കുറുക്കൻ അലസനായ നായയ്ക്ക് മുകളിലൂടെ ചാടുന്നു",
  "tamil": "வேகமாக பழுப்பு நிற நரி சோம்பேறி நாய் மீது குதிக்கிறது",
  "odia": "ଦ୍ରୁତ ବାଦାମୀ ଶିଆଳ ଅଳସୁଆ କୁକୁର ଉପରେ ଡେଇଁ ପଡ଼ିଲା",
  "bengali": "দ্রুত বাদামী শিয়াল অলস কুকুরের উপর ঝাঁপিয়ে পড়ে",
  "assamese": "দ্ৰুত বাদামী শিয়ালটোৱে অলস কুকুৰটোৰ ওপৰেৰে জাপ মাৰে",
  "manipuri_meitei": "ꯀ ꯭ ꯋꯤꯛ ꯕ ꯭ ꯔꯥꯎꯟ ꯐꯣꯛ ꯭ ꯁ ꯑꯗꯨꯅ ꯂꯖꯤ ꯗꯣꯒ ꯑꯗꯨꯒꯤ ꯃꯊꯛꯇ ꯆꯡꯉꯛꯏ ꯫"
}
```

2. Endpoint (/translate/[lang]) -> http://127.0.0.1:8000/translate/hindi

---

---

```json
body : {
    "text": "The quick brown fox jumps over the lazy dog."
}

response: {
  "result": "तेज़ भूरा लोमड़ी आलसी कुत्ते के ऊपर से कूदती है"
}
```

## Supported Languages

```json
"supported_languages": [
    "hindi",
    "urdu",
    "punjabi",
    "gujarati",
    "marathi",
    "telugu",
    "kannada",
    "malayalam",
    "tamil",
    "odia",
    "bengali",
    "assamese",
    "manipuri_meitei",
  ]
```
