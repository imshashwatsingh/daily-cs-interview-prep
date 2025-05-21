import json
import matplotlib.pyplot as plt
from datetime import datetime

HISTORY_FILE = "history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    history = load_history()
    dates = sorted(history.keys())
    daily_attempts = []
    daily_correct = []
    daily_incorrect = []
    custom_attempts = []
    custom_correct = []
    custom_incorrect = []
    for date in dates:
        attempts = history[date]
        daily = [a for a in attempts if a.get("action") == "daily"]
        custom = [a for a in attempts if a.get("action") != "daily"]
        # Daily
        daily_attempts.append(len(daily))
        daily_correct.append(sum(1 for a in daily if a.get("correct") is True))
        daily_incorrect.append(sum(1 for a in daily if a.get("correct") is False))
        # Custom
        custom_attempts.append(len(custom))
        custom_correct.append(sum(1 for a in custom if a.get("correct") is True))
        custom_incorrect.append(sum(1 for a in custom if a.get("correct") is False))
    plt.figure(figsize=(12,7))
    plt.subplot(2,1,1)
    plt.plot(dates, daily_attempts, label="Daily Attempted", marker='o')
    plt.plot(dates, daily_correct, label="Daily Correct", marker='o', color='green')
    plt.plot(dates, daily_incorrect, label="Daily Incorrect", marker='o', color='red')
    plt.title("Daily Question Results")
    plt.ylabel("Count")
    plt.legend()
    plt.xticks(rotation=45)
    plt.subplot(2,1,2)
    plt.plot(dates, custom_attempts, label="Custom Attempted", marker='o')
    plt.plot(dates, custom_correct, label="Custom Correct", marker='o', color='green')
    plt.plot(dates, custom_incorrect, label="Custom Incorrect", marker='o', color='red')
    plt.title("Custom Practice Results")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
