import json
import os

class Settings:
    def __init__(self, teacher_name="", teacher_email="", class_name="",
                 report_filter_enabled=False, grade_cutoff=None,
                 custom_message="", language="en"):
        self.teacher_name = teacher_name
        self.teacher_email = teacher_email
        self.class_name = class_name
        self.report_filter_enabled = report_filter_enabled
        self.grade_cutoff = grade_cutoff
        self.custom_message = custom_message
        self.language = language

    def to_dict(self):
        return {
            "teacher_name": self.teacher_name,
            "teacher_email": self.teacher_email,
            "class_name": self.class_name,
            "report_filter_enabled": self.report_filter_enabled,
            "grade_cutoff": self.grade_cutoff,
            "custom_message": self.custom_message,
            "language": self.language
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            teacher_name=data.get("teacher_name", ""),
            teacher_email=data.get("teacher_email", ""),
            class_name=data.get("class_name", ""),
            report_filter_enabled=data.get("report_filter_enabled", False),
            grade_cutoff=data.get("grade_cutoff"),
            custom_message=data.get("custom_message", ""),
            language=data.get("language", "en")
        )

    def save_to_file(self, filepath="user.settings"):
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath="user.settings"):
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                try:
                    data = json.load(f)
                    return cls.from_dict(data)
                except json.JSONDecodeError:
                    pass
        else:
            return DEFAULT_SETTINGS
        return cls()  # fallback if corrupted

DEFAULT_SETTINGS = Settings(
    teacher_name="Mr. Masini",
    teacher_email="connor.masini@detroitk12.org",
    class_name="AP Precalculus",
    report_filter_enabled=True,
    grade_cutoff=70,
    custom_message=(
        "Most of these assignments can still be turned in for partial credit, but they need to be turned in "
        "as soon as possible to avoid losing more points. These missing assignments are listed at the end of this letter."
    ),
    language="es"
)
