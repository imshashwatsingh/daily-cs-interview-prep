# Daily CS Interview Prep Bot

A beautiful, modern, and feature-rich desktop application for practicing Computer Science interview questions daily. Built with Python and Tkinter, this project helps you master CS fundamentals, track your progress, and get AI-powered explanations for every question.

---

## Features

- **Daily Question Mode:** Get a new MCQ every day, with streak tracking and logs.
- **Custom Practice:** Select topic and difficulty to practice as many MCQs as you want.
- **Large Question Bank:** 100+ high-quality MCQs across Data Structures, Algorithms, OS, DBMS, Networking, and OOP.
- **Beautiful GUI:** Modern, clean, and responsive interface with color-coded feedback for correct/incorrect answers.
- **Hints & Key Points:** Get hints and see key answer points for every question.
- **Gemini AI Integration:** Get detailed, AI-generated explanations for any question (requires Google Gemini API key).
- **Progress Visualization:** Visualize your daily and custom practice progress over time with interactive graphs.
- **Persistent History:** All attempts and results are logged for long-term tracking.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/imshashwatsingh/daily-cs-interview-prep.git
cd daily-cs-interview-prep
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8+
- `tkinter` (usually included with Python)
- `matplotlib` (for progress visualization)
- `python-dotenv` (for .env support)
- `google-generativeai` (for Gemini AI explanations)

### 3. Set Up Gemini API Key (Optional, for AI explanations)
- Create a `.env` file in the project root:
  ```
  GEMINI_API_KEY=your_google_gemini_api_key
  ```
- [Get your Gemini API key here.](https://aistudio.google.com/app/apikey)

### 4. Run the App
```bash
python bot.py
```

### 5. Visualize Progress
```bash
python visualize_progress.py
```

---

## File Structure

- `bot.py` - Main GUI application
- `questions.json` - Large MCQ question bank
- `history.json` - User's attempt and result logs
- `user_data.json` - User preferences and streaks
- `gemini_integration.py` - Gemini AI integration
- `visualize_progress.py` - Progress graph visualization
- `.env` - (Optional) Gemini API key

---

## How It Works

- **Daily Question:** Click "Get Daily Question" for a new MCQ every day. Your answer, correctness, and streak are logged.
- **Custom Practice:** Choose topic and difficulty to practice more MCQs. All attempts are logged.
- **Hints & Explanations:** Use the "Show Hint" and "Gemini Explanation" buttons for help and deep understanding.
- **Progress Graph:** See your improvement over time with `visualize_progress.py`.

---

## About the Developer

**Shashwat Singh**  
[GitHub](https://github.com/imshashwatsingh)  
This project is built and maintained by Shashwat Singh. Contributions, suggestions, and feedback are welcome!

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements
- Google Gemini for AI explanations
- Python, Tkinter, and the open-source community

---

## Contributing

Pull requests and issues are welcome! Please open an issue for bugs or feature requests.

---

**Happy Interview Prep!**
