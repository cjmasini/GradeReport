import tkinter as tk
from tkinter import Tk, Label, Entry, Button, Frame, PhotoImage, Checkbutton
from tkinter.font import Font
from logo import getWesternLogo, getSettingsIcon
from reportGenerator import generate_report
from settings import Settings
from filters import ScoreFilter
from studentSelector import StudentSelector
from progressBar import ProgressBar

class ReportUI:
    def __init__(self):
        self.log_label = None
        self.class_name = None
        self.teacher_name = None
        self.teacher_email = None
        self.class_hour = None
        self.logo = None
        self.settings_icon = None
        self.root = None
        self.custom_msg_expanded = False
        self.settings = Settings.load_from_file()

    def createUI(self):
        if self.root is None:
            self.root = Tk()
        else:
            for widget in self.root.winfo_children():
                widget.destroy()

        self.root.title("Grade Report Generator")
        self.root.configure(bg="#f8f9fa")
        self.root.geometry("475x650")

        top_bar = Frame(self.root, bg="#f8f9fa")
        top_bar.pack(side="top", fill="x")

        self.settings_icon = getSettingsIcon()
        settings_button = Button(top_bar, image=self.settings_icon, command=self.open_settings,
                                 bd=0, bg="#f8f9fa", activebackground="#f8f9fa", cursor="hand2")
        settings_button.image = self.settings_icon
        settings_button.pack(side="left", padx=10, pady=10)

        content_frame = Frame(self.root, bg="#f8f9fa")
        content_frame.pack(fill="both", expand=True)

        self.logo = getWesternLogo()
        if self.logo:
            logo_label = Label(content_frame, image=self.logo, bg="#f8f9fa")
            logo_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")
        else:
            error_label = Label(content_frame, text="Error loading logo", bg="#f8f9fa")
            error_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        custom_font = Font(family="Helvetica", size=12)
        input_frame = Frame(content_frame, bg="#ffffff", bd=2, relief="groove")
        input_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="n")

        Label(input_frame, text="Class Name:", font=custom_font, bg="#ffffff").grid(row=0, column=0, padx=10, pady=10)
        class_name_entry = Entry(input_frame, width=30, font=custom_font, highlightthickness=1,
                                 highlightbackground="#cccccc", highlightcolor="#cccccc")
        class_name_entry.insert(0, self.settings.class_name)
        class_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        Label(input_frame, text="Teacher Name:", font=custom_font, bg="#ffffff").grid(row=1, column=0, padx=10, pady=10)
        teacher_name_entry = Entry(input_frame, width=30, font=custom_font, highlightthickness=1,
                                   highlightbackground="#cccccc", highlightcolor="#cccccc")
        teacher_name_entry.insert(0, self.settings.teacher_name)
        teacher_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        Label(input_frame, text="Teacher Email:", font=custom_font, bg="#ffffff").grid(row=2, column=0, padx=10, pady=10)
        teacher_email_entry = Entry(input_frame, width=30, font=custom_font, highlightthickness=1,
                                    highlightbackground="#cccccc", highlightcolor="#cccccc")
        teacher_email_entry.insert(0, self.settings.teacher_email)
        teacher_email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="n")

        self.log_label = Label(content_frame, text="", font=("Helvetica", 10), bg="#f8f9fa", fg="blue")
        self.log_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.progress_bar = ProgressBar(content_frame, row=6)
        self.progress_bar.hide() 

        filters = []
        if self.settings.report_filter_enabled and self.settings.grade_cutoff is not None:
            filters.append(ScoreFilter(self.settings.grade_cutoff))

        Button(content_frame, text="Choose File", command=lambda: generate_report(
            self.log_label,
            self.settings,
            self.progress_bar,
            filters
        )).grid(row=4, column=0, pady=10, sticky="e", padx=10)

        Button(
            content_frame,
            text="Select Specific Students",
            command=self.open_student_selector
        ).grid(row=4, column=1, pady=10, sticky="w", padx=10)



        self.root.mainloop()

    def open_settings(self):
        self.root.geometry("525x700")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Settings")

        form_frame = Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        form_frame.pack(padx=30, pady=(10, 20), ipadx=10, ipady=10)
        form_frame.grid_columnconfigure(1, weight=1)

        font_label = Font(family="Helvetica", size=12)

        Label(form_frame, text="Program Defaults", font=("Helvetica", 18, "bold"), bg="#f8f9fa").grid(row=0, column=0, columnspan=2, pady=(0, 10))

        Label(form_frame, text="Default Teacher Name:", font=font_label, bg="#ffffff").grid(
            row=1, column=0, sticky="w", padx=10, pady=10
        )
        self.teacher_name_entry = Entry(form_frame, width=30, font=font_label,
                                        highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#cccccc")
        self.teacher_name_entry.insert(0, self.settings.teacher_name)
        self.teacher_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")

        Label(form_frame, text="Default Teacher Email:", font=font_label, bg="#ffffff").grid(
            row=2, column=0, sticky="w", padx=10, pady=10
        )
        self.teacher_email_entry = Entry(form_frame, width=30, font=font_label,
                                         highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#cccccc")
        self.teacher_email_entry.insert(0, self.settings.teacher_email)
        self.teacher_email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")

        Label(form_frame, text="Default Class Name:", font=font_label, bg="#ffffff").grid(
            row=3, column=0, sticky="w", padx=10, pady=10
        )
        self.class_name_entry = Entry(form_frame, width=30, font=font_label,
                                      highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#cccccc")
        self.class_name_entry.insert(0, self.settings.class_name)
        self.class_name_entry.grid(row=3, column=1, padx=10, pady=10, sticky="we")

        report_frame = Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        report_frame.pack(padx=30, pady=(10, 20), ipadx=10, ipady=10)
        report_frame.grid_columnconfigure(1, weight=1)

        Label(report_frame, text="Report Settings", font=("Helvetica", 14, "bold"), bg="#ffffff").grid(
            row=0, column=0, columnspan=2, pady=(0, 10)
        )

        self.report_filter_var = tk.BooleanVar(value=self.settings.report_filter_enabled)

        self.report_filter_checkbox = Checkbutton(
            report_frame,
            text="Enable grade cutoff filter",
            variable=self.report_filter_var,
            onvalue=True,
            offvalue=False,
            bg="#ffffff",
            font=font_label,
            command=self.toggle_grade_cutoff_entry
        )
        self.report_filter_checkbox.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        self.grade_cutoff_label = Label(report_frame, text="Only for grades <", font=font_label, bg="#ffffff")
        self.grade_cutoff_entry = Entry(report_frame, width=10, font=font_label,
                                        highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#cccccc")
        if self.settings.grade_cutoff is not None:
            self.grade_cutoff_entry.insert(0, str(self.settings.grade_cutoff))

        if self.settings.report_filter_enabled:
            self.grade_cutoff_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
            self.grade_cutoff_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # --- Custom Report Message Frame ---
        self.custom_msg_frame = Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        self.custom_msg_frame.pack(padx=30, pady=(5, 10), fill="x")

        header_frame = Frame(self.custom_msg_frame, bg="#ffffff")
        header_frame.pack(fill="x")

        Label(header_frame, text="Modify Message", font=("Helvetica", 14, "bold"), bg="#ffffff").pack(side="left", padx=10, pady=5)
        self.expand_btn = Button(header_frame, text="▼", width=2, command=self.toggle_custom_msg_frame, bg="#ffffff", bd=0, font=("Helvetica", 12))
        self.expand_btn.pack(side="right", padx=10)

        self.custom_msg_content = Frame(self.custom_msg_frame, bg="#ffffff")
        self.custom_msg_content.pack(fill="x")

        self.custom_message_entry = tk.Text(self.custom_msg_content, width=40, height=4, font=font_label,
            highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#cccccc", wrap="word")
        self.custom_message_entry.insert("1.0", self.settings.custom_message or "")
        self.custom_message_entry.pack(padx=10, pady=5, fill="x")

        self.custom_msg_content.forget()
        self.custom_msg_expanded = False

        save_btn = Button(self.root, text="Save Settings", font=("Helvetica", 12, "bold"),
                          command=self.save_settings, bg="#007bff", fg="white", padx=20, pady=5)
        save_btn.pack(pady=20)

        # Dropdown for language
        Label(form_frame, text="Default Language:", font=font_label, bg="#ffffff").grid(
            row=4, column=0, sticky="w", padx=10, pady=10
        )

        self.language_var = tk.StringVar(value=self.settings.language)
        language_dropdown = tk.OptionMenu(
            form_frame,
            self.language_var,
            "en", "es", "ar"
        )
        language_dropdown.config(font=font_label, bg="#ffffff", width=10)
        language_dropdown.grid(row=4, column=1, padx=10, pady=10, sticky="w")


    def toggle_grade_cutoff_entry(self):
        if self.report_filter_var.get():
            self.grade_cutoff_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
            self.grade_cutoff_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        else:
            self.grade_cutoff_label.grid_remove()
            self.grade_cutoff_entry.grid_remove()

    def toggle_custom_msg_frame(self):
        if self.custom_msg_expanded:
            self.custom_msg_content.forget()
            self.expand_btn.config(text="▼")
            self.custom_msg_expanded = False
        else:
            self.custom_msg_content.pack(fill="x")
            self.expand_btn.config(text="▲")
            self.custom_msg_expanded = True

    def save_settings(self):
        self.settings.teacher_name = self.teacher_name_entry.get()
        self.settings.teacher_email = self.teacher_email_entry.get()
        self.settings.class_name = self.class_name_entry.get()
        self.settings.report_filter_enabled = self.report_filter_var.get()
        self.settings.custom_message = self.custom_message_entry.get("1.0", "end").strip()
        self.settings.language = self.language_var.get()

        if self.settings.report_filter_enabled:
            try:
                val = float(self.grade_cutoff_entry.get())
                if 0 <= val <= 100:
                    self.settings.grade_cutoff = val
                else:
                    self.settings.grade_cutoff = None
            except ValueError:
                self.settings.grade_cutoff = None
        else:
            self.settings.grade_cutoff = None

        self.settings.save_to_file()
        self.createUI()

        if self.log_label:
            self.log_label.config(text="Settings saved.")

    def open_student_selector(self):
        selector = StudentSelector(self.log_label, self.settings, self.progress_bar)
        selector.open()

ReportUI().createUI()
