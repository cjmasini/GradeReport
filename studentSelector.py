import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from reportGenerator import parse_students, generate_report_for_selected, open_file, select_file
from settings import Settings
from language_map import LANGUAGE_MAP, update_language

class StudentSelector:
    def __init__(self, log_label, settings: Settings, progress_bar):
        self.log_label = log_label
        self.settings = settings
        self.progress_bar = progress_bar
        self.students = []
        self.selected = {}
        self.languages = {}

    def open(self):
        filename = select_file()
        self.students = parse_students(filename, self.log_label, self.settings)
        self.selected = {student.name: tk.BooleanVar(value=True) for student in self.students}
        self.languages = {student.name: tk.StringVar(value=self.settings.language) for student in self.students}

        self.root = tk.Toplevel()
        self.root.title("Select Students")
        self.root.geometry("800x600")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=5)

        self.canvas = tk.Canvas(self.root)
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.frame_width)

        header = tk.Frame(self.frame)
        header.pack(fill="x", pady=2)
        tk.Label(header, text="Student Name", width=17, anchor="w", font=("Helvetica", 10, "bold")).pack(side="left")
        tk.Label(header, text="Grade", width=9, anchor="w", font=("Helvetica", 10, "bold")).pack(side="left")
        tk.Label(header, text="Language", width=12, anchor="w", font=("Helvetica", 10, "bold")).pack(side="left")
        tk.Label(header, text="Include", width=10, anchor="w", font=("Helvetica", 10, "bold")).pack(side="left")
        select_all_var = tk.BooleanVar(value=True)
        select_all_cb = tk.Checkbutton(header, text="Select All", variable=select_all_var,
                                       command=lambda: self.toggle_all(select_all_var.get()))
        select_all_cb.pack(anchor="w")
        for student in self.students:
            row = tk.Frame(self.frame)
            row.pack(fill="x", pady=1)

            tk.Label(row, text=student.name, width=20, anchor="w").pack(side="left")
            tk.Label(row, text=student.percent, width=10, anchor="w").pack(side="left")

            initial_lang = LANGUAGE_MAP.get(self.languages[student.name].get(), "Spanish")
            display_var = tk.StringVar(value=initial_lang)
            lang_menu = ttk.Combobox(row, textvariable=display_var, values=list(LANGUAGE_MAP.values()), width=10)
            lang_menu.pack(side="left", padx=5)
            display_var.trace_add("write", lambda *_, var=display_var, name=student.name: update_language(self.languages, var, name))

            cb = tk.Checkbutton(row, variable=self.selected[student.name])
            cb.pack(side="left", padx=5)

        bottom = tk.Frame(self.root)
        bottom.pack(pady=10)

        tk.Button(bottom, text="Generate Report", command=self.generate).pack()

    def toggle_all(self, state):
        for var in self.selected.values():
            var.set(state)

    def frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def generate(self):
        selected_students = [
            (s, self.languages[s.name].get())
            for s in self.students
            if self.selected[s.name].get()
        ]
        print(f"Selected students: {len(selected_students)}")

        self.log_label["text"]=f"{len(selected_students)} students selected."
        self.log_label.update()

        if not selected_students:
            self.log_label["text"]="No students selected."
            self.log_label.update()
            return

        generate_report_for_selected(
            self.log_label, self.settings, selected_students, self.progress_bar)

