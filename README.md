# Translate-API

## Setup Locally

```bash
git clone https://github.com/cse21mce/translate-api.git
```

## Package Installatoin

```bash
pip install torch
pip install transformers
git clone https://github.com/VarunGumma/IndicTransTokenizer
cd IndicTransTokenizer

pip install --editable ./
```

## Usage

1. Endpoint (/translate) -> http://127.0.0.1:8000/translate

---

---

```json
body : {
    "text": "The President of India"
}

response: {
    "punjabi" : ["ਭਾਰਤ ਦੇ ਰਾਸ਼ਟਰਪਤੀ "],
    "bengali" : ["ভারতের রাষ্ট্রপতি "],
    "malayalam" : ["ഇന്ത്യയുടെ രാഷ്ട്രപതി "],
    "marathi" : ["भारताचे राष्ट्रपती "],
    "tamil" : ["இந்திய குடியரசுத் தலைவர் "],
    "gujarati" : ["ભારતના રાષ્ટ્રપતિ "],
    "telugu" : ["భారత రాష్ట్రపతి "],
    "hindi" : ["भारत के राष्ट्रपति "],
    "urdu" : ["ہندوستان کے صدر "],
    "kannada" : ["ಭಾರತದ ರಾಷ್ಟ್ರಪತಿ "]
}
```

2. Endpoint (/translate/[lang]) -> http://127.0.0.1:8000/translate/hindi

---

---

```json
body : {
    "text": "The President of India"
}

response: {
  "result": "भारत के राष्ट्रपति"
}
```
