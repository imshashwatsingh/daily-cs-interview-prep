import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
from datetime import datetime
import random
import os
from gemini_integration import get_gemini_explanation

QUESTIONS_FILE = "questions.json"
HISTORY_FILE = "history.json"

# --- Helper Functions ---
def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        return []
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_today_key():
    return datetime.now().strftime("%Y-%m-%d")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def get_daily_question():
    questions = load_questions()
    if not questions:
        return None
    today = get_today_key()
    random.seed(today)
    return questions[random.randint(0, len(questions)-1)]

def get_questions_by_topic_and_difficulty(topic, difficulty):
    questions = load_questions()
    return [
        q for q in questions
        if (q["topic"] == topic or topic == "Any")
        and (q["difficulty"] == difficulty or difficulty == "Any")
    ]

def save_progress(question_id, action, selected_option=None, correct=None):
    today = get_today_key()
    history = load_history()
    if today not in history:
        history[today] = []
    entry = {
        "question_id": question_id,
        "action": action,
        "timestamp": datetime.now().isoformat()
    }
    if selected_option is not None:
        entry["selected_option"] = selected_option
    if correct is not None:
        entry["correct"] = correct
    history[today].append(entry)
    save_history(history)

def has_attempted_today(question_id):
    today = get_today_key()
    history = load_history()
    if today in history:
        for entry in history[today]:
            if entry.get("question_id") == question_id:
                return True
    return False

TOPICS = ["Data Structures", "Algorithms", "Operating Systems", "DBMS", "Networking", "OOP"]
DIFFICULTIES = ["Easy", "Medium", "Hard", "Any"]

class CSInterviewPrepApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Daily CS Interview Prep (Enhanced)")
        self.geometry("950x750")
        self.configure(bg="#e9ecef")
        self.style_font = ("Segoe UI", 14)
        self.header_font = ("Segoe UI", 22, "bold")
        self.button_font = ("Segoe UI", 13, "bold")
        self.radio_font = ("Segoe UI", 13)
        self.fg_color = "#22223b"
        self.accent_color = "#4f8cff"
        self.correct_color = "#4caf50"
        self.wrong_color = "#e63946"
        self.neutral_color = "#f0f4f8"
        self.current_question = None
        self.selected_option = tk.IntVar()
        self.asked_questions = set()
        self.build_gui()

    def build_gui(self):
        self.start_frame = tk.Frame(self, bg="#e9ecef")
        self.custom_select_frame = tk.Frame(self, bg="#e9ecef")
        self.question_frame = tk.Frame(self, bg="#e9ecef")
        self.start_frame.pack(fill="both", expand=True)

        tk.Label(self.start_frame, text="Welcome to Daily CS Interview Prep!", font=self.header_font, fg=self.accent_color, bg="#e9ecef").pack(pady=30)
        tk.Button(self.start_frame, text="Get Daily Question", font=self.button_font, bg=self.accent_color, fg="white", command=self.get_daily_question, width=22, height=2, bd=0, relief="ridge", cursor="hand2").pack(pady=15)
        tk.Button(self.start_frame, text="Practice More MCQs", font=self.button_font, bg="#22223b", fg="white", command=self.get_custom_question, width=22, height=2, bd=0, relief="ridge", cursor="hand2").pack(pady=10)
        tk.Button(self.start_frame, text="View Progress Graph", font=self.button_font, bg="#43aa8b", fg="white", command=self.open_progress_graph, width=22, height=2, bd=0, relief="ridge", cursor="hand2").pack(pady=10)

        # Custom select frame
        tk.Label(self.custom_select_frame, text="Select Topic:", font=self.style_font, bg="#e9ecef").pack(pady=10)
        self.topic_var = tk.StringVar(value=TOPICS[0])
        self.topic_menu = tk.OptionMenu(self.custom_select_frame, self.topic_var, *TOPICS)
        self.topic_menu.config(font=self.style_font)
        self.topic_menu.pack()
        tk.Label(self.custom_select_frame, text="Select Difficulty:", font=self.style_font, bg="#e9ecef").pack(pady=10)
        self.difficulty_var = tk.StringVar(value=DIFFICULTIES[0])
        self.difficulty_menu = tk.OptionMenu(self.custom_select_frame, self.difficulty_var, *DIFFICULTIES)
        self.difficulty_menu.config(font=self.style_font)
        self.difficulty_menu.pack()
        tk.Button(self.custom_select_frame, text="Fetch Question", font=self.button_font, bg=self.accent_color, fg="white", command=self.fetch_custom_question, width=18, bd=0, relief="ridge", cursor="hand2").pack(pady=20)
        tk.Button(self.custom_select_frame, text="Back to Menu", font=self.button_font, bg="#e63946", fg="white", command=self.back_to_menu, width=14, bd=0, relief="ridge", cursor="hand2").pack(pady=10)

        # Question frame
        self.question_title = tk.Label(self.question_frame, text="", font=self.header_font, fg=self.accent_color, bg="#e9ecef")
        self.question_title.pack(pady=10)
        self.question_desc = tk.Label(self.question_frame, text="", font=self.style_font, wraplength=850, justify="left", bg="#e9ecef", fg=self.fg_color)
        self.question_desc.pack(pady=10)
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.question_frame, text="", variable=self.selected_option, value=i, font=self.radio_font, bg=self.neutral_color, anchor="w", width=60, indicatoron=0, selectcolor="#dbeafe", pady=8, bd=2, relief="groove", cursor="hand2")
            rb.pack(pady=6, padx=60, anchor="w")
            self.radio_buttons.append(rb)
        self.submit_button = tk.Button(self.question_frame, text="Submit Answer", font=self.button_font, bg=self.accent_color, fg="white", command=self.submit_answer, width=18, bd=0, relief="ridge", cursor="hand2")
        self.submit_button.pack(pady=10)
        self.next_button = tk.Button(self.question_frame, text="Next Question", font=self.button_font, bg="#43aa8b", fg="white", command=self.next_question, width=18, bd=0, relief="ridge", cursor="hand2")
        self.next_button.pack(pady=5)
        self.hint_button = tk.Button(self.question_frame, text="Show Hint", font=self.button_font, bg="#22223b", fg="white", command=self.show_hint, width=14, bd=0, relief="ridge", cursor="hand2")
        self.hint_button.pack(side="left", padx=10, pady=10)
        self.gemini_button = tk.Button(self.question_frame, text="Gemini Explanation", font=self.button_font, bg="#4f8cff", fg="white", command=self.show_gemini_explanation, width=18, bd=0, relief="ridge", cursor="hand2")
        self.gemini_button.pack(side="left", padx=10, pady=10)
        self.back_button = tk.Button(self.question_frame, text="Back to Menu", font=self.button_font, bg="#e63946", fg="white", command=self.back_to_menu, width=14, bd=0, relief="ridge", cursor="hand2")
        self.back_button.pack(side="left", padx=10, pady=10)
        self.feedback_label = tk.Label(self.question_frame, text="", font=self.style_font, bg="#e9ecef")
        self.feedback_label.pack(pady=10)
        self.answer_text = scrolledtext.ScrolledText(self.question_frame, wrap=tk.WORD, height=7, font=self.style_font, bg="#f8fafc", fg=self.fg_color)
        self.answer_text.pack(pady=10, fill="both", expand=True)

    def get_daily_question(self):
        question = get_daily_question()
        if question is None:
            messagebox.showerror("Error", "No questions available.")
            return
        self.show_question(question)

    def get_custom_question(self):
        self.start_frame.pack_forget()
        self.custom_select_frame.pack(fill="both", expand=True)

    def fetch_custom_question(self):
        topic = self.topic_var.get()
        difficulty = self.difficulty_var.get()
        questions = load_questions()
        # Only filter by topic and difficulty, and show all matching questions in sequence
        filtered = [q for q in questions if (q["topic"] == topic or topic == "Any") and (q["difficulty"] == difficulty or difficulty == "Any")]
        if not filtered:
            messagebox.showerror("Error", "No questions found for the selected topic and difficulty.")
            return
        self.filtered_questions = filtered
        self.filtered_index = 0
        self.show_question(self.filtered_questions[self.filtered_index])
        self.custom_select_frame.pack_forget()

    def show_question(self, question):
        self.start_frame.pack_forget()
        self.custom_select_frame.pack_forget()
        self.question_frame.pack(fill="both", expand=True)
        self.current_question = question
        self.asked_questions.add(question['id'])
        self.selected_option.set(-1)
        self.question_title.config(text=f"{question['topic']} ({question['difficulty']})")
        self.question_desc.config(text=question.get("question", "No description available."))
        options = question.get("options", ["Option 1", "Option 2", "Option 3", "Option 4"])
        for i, rb in enumerate(self.radio_buttons):
            rb.config(text=options[i] if i < len(options) else "", state="normal", bg=self.neutral_color, fg=self.fg_color)
        self.feedback_label.config(text="")
        self.answer_text.delete(1.0, tk.END)
        self.submit_button.config(state="normal")
        self.next_button.config(state="disabled")

    def submit_answer(self):
        if self.current_question is None:
            messagebox.showerror("Error", "No question loaded.")
            return
        selected = self.selected_option.get()
        if selected == -1:
            messagebox.showwarning("No Selection", "Please select an option before submitting.")
            return
        correct = (selected == self.current_question.get("correct_option", -1))
        for i, rb in enumerate(self.radio_buttons):
            if i == self.current_question.get("correct_option", -1):
                rb.config(bg=self.correct_color, fg="white")
            elif i == selected:
                rb.config(bg=self.wrong_color if not correct else self.correct_color, fg="white")
            else:
                rb.config(bg=self.neutral_color, fg=self.fg_color)
        if correct:
            self.feedback_label.config(text="Correct! Well done!", fg=self.correct_color)
        else:
            self.feedback_label.config(text=f"Incorrect. The correct answer is: {self.current_question['options'][self.current_question['correct_option']]}", fg=self.wrong_color)
        self.submit_button.config(state="disabled")
        self.next_button.config(state="normal")
        save_progress(self.current_question["id"], "attempted", selected_option=selected, correct=correct)
        self.show_answer_text()

    def next_question(self):
        # If in custom mode, go to next in filtered list
        if hasattr(self, 'filtered_questions') and self.filtered_questions:
            self.filtered_index += 1
            if self.filtered_index >= len(self.filtered_questions):
                messagebox.showinfo("End", "No more questions for this topic/difficulty.")
                self.back_to_menu()
                return
            self.show_question(self.filtered_questions[self.filtered_index])
        else:
            # Default: pick a random new question (not already asked in this session)
            questions = load_questions()
            available = [q for q in questions if q['id'] not in self.asked_questions]
            if not available:
                self.asked_questions = set()
                available = questions
            question = random.choice(available)
            self.show_question(question)

    def show_hint(self):
        if self.current_question is None:
            messagebox.showerror("Error", "No question loaded.")
            return
        hint = self.current_question.get("hint", "No hint available.")
        messagebox.showinfo("Hint", hint)

    def show_answer_text(self):
        keywords = self.current_question.get("answer_keywords", [])
        answer = "Key points to mention:\n" + "\n".join(f"- {kw}" for kw in keywords) if keywords else "No answer available."
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, answer)

    def show_gemini_explanation(self):
        if self.current_question is None:
            messagebox.showerror("Error", "No question loaded.")
            return
        selected = self.selected_option.get()
        user_answer = self.current_question["options"][selected] if selected != -1 else None
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, "Fetching Gemini explanation... Please wait.")
        self.update()
        explanation = get_gemini_explanation(self.current_question.get("question", ""), user_answer)
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, explanation)

    def back_to_menu(self):
        self.current_question = None
        self.question_frame.pack_forget()
        self.start_frame.pack(fill="both", expand=True)

    def open_progress_graph(self):
        import subprocess
        subprocess.Popen(["python", "visualize_progress.py"])

if __name__ == "__main__":
    app = CSInterviewPrepApp()
    app.mainloop()