from typing import List, Tuple
from student import Student

class Filter:
    def apply(self, student: 'Student') -> bool:
        raise NotImplementedError("Filter subclasses must implement the apply method.")

class ScoreFilter(Filter):
    def __init__(self, cutoff):
        self.cutoff = cutoff

    def apply(self, student: 'Student') -> bool:
        return student.getGrade() < self.cutoff

class SelectedStudentsFilter(Filter):
    def __init__(self, allowed_names):
        self.allowed_names = allowed_names  # just a set of strings (student names)

    def apply(self, student: 'Student') -> bool:
        return student.name in self.allowed_names

    def get_language(self, student: 'Student') -> str:
        return self.language_map.get(student.name, "en")
