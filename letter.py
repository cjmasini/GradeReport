from translate import translate

class LetterWriter:
    def __init__(self, name, email, language, customMessage):
        self.teacher_name = name
        self.teacher_email = email
        self.language = language
        self.customMessage = customMessage

        # English message
        self.message  = "To the Parent/Guardian of {},\n"
        self.message += "\tThis letter is to let you know that {} currently has a grade of {} ({}) in their {} class and has {} missing assignments. "
        self.message += customMessage + " "
        self.message += "If you have any questions or concerns, please do not hesitate to contact me at {}\n\n"

        # Arabic-specific wrapping for LTR content
        if language == "ar":
            LTR = "\u202A"
            PDF = "\u202C"
        else:
            LTR = ""
            PDF = ""

        # Pre-insert email before translating so it flows naturally
        translated_closing = translate(
            f"If you have any questions or concerns, please do not hesitate to contact me at {email}",
            language
        )

        self.translatedMessage  = translate("To the Parent/Guardian of", language) + f" {LTR}{{}}{PDF},\n"
        self.translatedMessage += "\t" + translate("This letter is to let you know that", language) + f" {LTR}{{}}{PDF} "
        self.translatedMessage += translate("currently has a grade of", language) + f" {LTR}{{}} ({{}}){PDF} "
        self.translatedMessage += translate("in their", language) + f" {LTR}{{}}{PDF} "
        self.translatedMessage += translate("class and has", language) + f" {LTR}{{}}{PDF} "
        self.translatedMessage += translate("missing assignments.", language) + " "
        self.translatedMessage += translate(customMessage, language) + " "
        self.translatedMessage += translated_closing + "\n\n"

    def generateLetter(self, student):
        text = self.message.format(
            student.name,
            student.first_name,
            student.percent,
            student.grade,
            student.subject,
            len(student.missingAssignments),
            self.teacher_email
        )

        text += self.translatedMessage.format(
            student.name,
            student.first_name,
            student.percent,
            student.grade,
            student.subject,
            len(student.missingAssignments)
        )

        if len(student.missingAssignments) > 0:
            text += "\n\nMissing Assignments / " + translate("Missing Assignments", self.language) + ":\n"
            for assignment in student.missingAssignments:
                text += "\t{}\n".format(assignment)
            text += "Student Name / " + translate("Student Name", self.language) + ": _______________________________\n\n"
            text += "Parent Name / " + translate("Parent Name", self.language) + ": _______________________________\n\n"
            text += "Parent Signature / " + translate("Parent Signature", self.language) + ": _______________________________\n\n"
            text += "Date / " + translate("Date", self.language) + ": _______________________________\n\n"

        text += "{}\n{} Teacher\n{}".format(self.teacher_name, student.subject, self.teacher_email)
        return text
