from translate import translate

class LetterWriter:
    def __init__(self, name, email, language, customMessage, progress_bar):
        self.teacher_name = name
        self.teacher_email = email
        self.language = language
        self.customMessage = customMessage
        self.shouldTranslate = True
        self.progress_bar = progress_bar

        self.message  = "To the Parent/Guardian of {},\n"
        self.message += "\tThis letter is to let you know that {} currently has a grade of {} ({}) in their {} class and has {} missing assignments. "
        self.message += customMessage + " "
        self.message += "If you have any questions or concerns, please do not hesitate to contact me at {}\n\n"

        # Arabic-specific wrapping for LTR content
        if language == "en":
            self.shouldTranslate = False
        elif language == "ar":
            LTR = "\u202A"
            PDF = "\u202C"
        else:
            LTR = ""
            PDF = ""

        self.translatedMessage = ""
        self.missingAssignments = ""
        self.forms = ""
        if self.shouldTranslate:
            self.translatedMessage += translate("To the Parent/Guardian of", language) + f" {LTR}{{}}{PDF},\n"
            self.translatedMessage += "\t" + translate("This letter is to let you know that", language) + f" {LTR}{{}}{PDF} "
            self.progress_bar.update(30)
            self.translatedMessage += translate("currently has a grade of", language) + f" {LTR}{{}} ({{}}){PDF} "
            self.translatedMessage += translate("in their", language) + f" {LTR}{{}}{PDF} "
            self.progress_bar.update(40)
            self.translatedMessage += translate("class and has", language) + f" {LTR}{{}}{PDF} "
            self.translatedMessage += translate("missing assignments.", language) + " "
            self.progress_bar.update(50)
            self.translatedMessage += translate(customMessage, language) + " "
            self.translatedMessage += translate(f"If you have any questions or concerns, please do not hesitate to contact me at {email}", language) + "\n\n"
            self.progress_bar.update(60)
            
            self.missingAssignments = "\n\nMissing Assignments / " + translate("Missing Assignments", self.language) + ":\n"

            self.forms += "Student Name / " + translate("Student Name", self.language) + ": _______________________________\n\n"
            self.progress_bar.update(70)
            self.forms += "Parent Name / " + translate("Parent Name", self.language) + ": _______________________________\n\n"
            self.progress_bar.update(80)
            self.forms += "Parent Signature / " + translate("Parent Signature", self.language) + ": _______________________________\n\n"
            self.forms += "Date / " + translate("Date", self.language) + ": _______________________________\n\n"
            self.progress_bar.update(90)
        else:
            self.forms += "Student Name: _______________________________\n\n"
            self.forms += "Parent Name: _______________________________\n\n"
            self.forms += "Parent Signature: _______________________________\n\n"
            self.forms += "Date: _______________________________\n\n"

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

        if self.shouldTranslate:
            text += self.translatedMessage.format(
                student.name,
                student.first_name,
                student.percent,
                student.grade,
                student.subject,
                len(student.missingAssignments)
            )

        if len(student.missingAssignments) > 0:
            text += self.missingAssignments
            for assignment in student.missingAssignments:
                text += "\t{}\n".format(assignment)
        
        text += self.forms
        text += "{}\n{} Teacher\n{}".format(self.teacher_name, student.subject, self.teacher_email)

        self.progress_bar.update(90)
        return text
