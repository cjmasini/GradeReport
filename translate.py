import requests

def translate(text, target_language="es"):
    try:
        if not text.strip():
            return text

        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"en|{target_language}"
        }
        print(f"Translating text: {text} to {target_language}")

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        return data.get("responseData", {}).get("translatedText", text)

    except Exception as e:
        print(f"Translation error: {e}")
        return text