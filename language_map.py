LANGUAGE_MAP = {
    "en": "English",
    "es": "Spanish",
    "ar": "Arabic"
}

LANGUAGE_REVERSE_MAP = {v: k for k, v in LANGUAGE_MAP.items()}

def update_language(languages, var, student_name):
    languages[student_name].set(LANGUAGE_REVERSE_MAP.get(var.get(), "en"))