import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure your API key
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def get_gemini_explanation(question, user_answer=None):
    """
    Fetches a detailed explanation for a CS concept or evaluates a user's answer
    using the Gemini API.
    """
    if not api_key:
        return "Error: Gemini API key not configured. Please set the GEMINI_API_KEY in your .env file."

    model = genai.GenerativeModel('gemini-pro')  # Using gemini-pro for detailed explanations

    prompt = f"Provide a detailed and concise explanation for the following Computer Science concept, suitable for an interview context:\n\nQuestion: {question}\n\n"
    if user_answer:
        prompt += f"Additionally, briefly assess the following user attempt for correctness and completeness:\nUser Answer: {user_answer}\n"
    prompt += "Focus on key definitions, common use cases, advantages, disadvantages, and relevant examples. Format the answer clearly with headings and bullet points where appropriate."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while fetching explanation from Gemini API: {e}"

if __name__ == "__main__":
    # This is for testing the Gemini integration
    # Make sure GEMINI_API_KEY is set in your .env file
    test_question = "What is a binary search tree?"
    explanation = get_gemini_explanation(test_question)
    print(f"Gemini Explanation for '{test_question}':\n{explanation}")

    test_question_with_answer = "Explain the difference between TCP and UDP."
    user_attempt = "TCP is reliable and connection-oriented, UDP is fast and connectionless."
    explanation_with_feedback = get_gemini_explanation(test_question_with_answer, user_attempt)
    print(f"\nGemini Explanation with feedback for '{test_question_with_answer}' (User's answer: '{user_attempt}'):\n{explanation_with_feedback}")